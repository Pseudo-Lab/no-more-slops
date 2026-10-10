-- 킁킁지도 스키마. Supabase 대시보드 > SQL Editor 에 통째로 붙여넣고 Run.
-- 로그인 없는 MVP: 브라우저마다 생성되는 device_id 로 "내 강아지"와 하트를 구분한다.

create table if not exists dogs (
  id uuid primary key default gen_random_uuid(),
  device_id text not null,
  name text not null check (char_length(name) between 1 and 20),
  breed text,
  age text,
  intro text check (char_length(intro) <= 60),
  avatar_url text,
  created_at timestamptz not null default now()
);

create table if not exists places (
  id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(name) between 1 and 40),
  lat double precision not null,
  lng double precision not null,
  created_at timestamptz not null default now()
);

create table if not exists posts (
  id uuid primary key default gen_random_uuid(),
  place_id uuid not null references places(id) on delete cascade,
  dog_id uuid not null references dogs(id) on delete cascade,
  photo_url text not null,
  caption text check (char_length(caption) <= 80),
  taken_at timestamptz,
  heart_count int not null default 0,
  created_at timestamptz not null default now()
);

create table if not exists hearts (
  post_id uuid not null references posts(id) on delete cascade,
  device_id text not null,
  primary key (post_id, device_id)
);

create index if not exists posts_place_idx on posts(place_id);

-- 하트 토글: 누르면 +1, 다시 누르면 -1. 새 하트 수를 돌려준다.
create or replace function toggle_heart(p_post uuid, p_device text)
returns int language plpgsql security definer set search_path = public as $$
declare n int;
begin
  if exists (select 1 from hearts where post_id = p_post and device_id = p_device) then
    delete from hearts where post_id = p_post and device_id = p_device;
    update posts set heart_count = heart_count - 1 where id = p_post returning heart_count into n;
  else
    insert into hearts(post_id, device_id) values (p_post, p_device);
    update posts set heart_count = heart_count + 1 where id = p_post returning heart_count into n;
  end if;
  return n;
end $$;

-- 내 강아지 수정: 등록한 브라우저(device_id)만 고칠 수 있다. 사진을 안 바꾸면 기존 사진 유지.
create or replace function update_dog(p_id uuid, p_device text, p_name text, p_breed text, p_age text, p_intro text, p_avatar_url text)
returns dogs language plpgsql security definer set search_path = public as $$
declare d dogs;
begin
  update dogs set name = p_name, breed = p_breed, age = p_age, intro = p_intro,
    avatar_url = coalesce(p_avatar_url, avatar_url)
  where id = p_id and device_id = p_device
  returning * into d;
  if d.id is null then raise exception '내 강아지만 수정할 수 있어요'; end if;
  return d;
end $$;

-- 누구나 읽고 올릴 수 있게 (수정/삭제는 막음)
alter table dogs enable row level security;
alter table places enable row level security;
alter table posts enable row level security;
alter table hearts enable row level security;

drop policy if exists "read dogs" on dogs;      create policy "read dogs" on dogs for select using (true);
drop policy if exists "add dogs" on dogs;       create policy "add dogs" on dogs for insert with check (true);
drop policy if exists "read places" on places;  create policy "read places" on places for select using (true);
drop policy if exists "add places" on places;   create policy "add places" on places for insert with check (true);
drop policy if exists "read posts" on posts;    create policy "read posts" on posts for select using (true);
drop policy if exists "add posts" on posts;     create policy "add posts" on posts for insert with check (heart_count = 0);
drop policy if exists "read hearts" on hearts;  create policy "read hearts" on hearts for select using (true);

grant execute on function toggle_heart(uuid, text) to anon, authenticated;
grant execute on function update_dog(uuid, text, text, text, text, text, text) to anon, authenticated;

-- 사진 저장소 (공개 읽기, 누구나 업로드)
insert into storage.buckets (id, name, public) values ('photos', 'photos', true)
on conflict (id) do nothing;

drop policy if exists "upload photos" on storage.objects;
create policy "upload photos" on storage.objects for insert to anon, authenticated
  with check (bucket_id = 'photos');

-- 길고양이: 등록된 강아지(dog_id) 대신 무늬(cat_type)와 동네에서 부르는 이름(cat_name)으로 남긴다.
alter table posts alter column dog_id drop not null;
alter table posts add column if not exists cat_type text;
alter table posts add column if not exists cat_name text check (char_length(cat_name) <= 20);
alter table posts drop constraint if exists posts_who;
alter table posts add constraint posts_who check (dog_id is not null or cat_type is not null);

-- 욕설 막기: 브라우저에서 먼저 막고, 우회해서 보내도 DB에서 한 번 더 막는다.
-- 한글·영문만 남겨서 검사 ("시 1 발" 같은 우회 대응). src/moderation.js 의 목록과 맞춘다.
create or replace function has_bad_words(t text) returns boolean language sql immutable as $$
  select coalesce(regexp_replace(lower(t), '[^가-힣ㄱ-ㅎa-z]', '', 'g'), '') ~
    '(시발|씨발|씨바|씨빨|시빨|쓰발|ㅅㅂ|ㅆㅂ|ㅄ|ㅂㅅ|병신|븅신|빙신|병쉰|개새끼|개색기|개색끼|개세끼|개쌔끼|개새기|좆|존나|졸라|ㅈㄴ|지랄|ㅈㄹ|미친놈|미친년|미친새끼|또라이|엠창|느금|니애미|니어미|니미|썅|쌍년|쌍놈|걸레년|창녀|꺼져|닥쳐|fuck|shit|bitch|asshole)'
$$;

create or replace function block_bad_words() returns trigger language plpgsql as $$
declare v text;
begin
  foreach v in array tg_argv loop
    if has_bad_words(to_jsonb(new) ->> v) then
      raise exception '욕설이나 비하 표현은 올릴 수 없어요. 고운 말로 적어주세요.';
    end if;
  end loop;
  return new;
end $$;

drop trigger if exists dogs_bad_words on dogs;
create trigger dogs_bad_words before insert or update on dogs for each row execute function block_bad_words('name', 'breed', 'age', 'intro');
drop trigger if exists places_bad_words on places;
create trigger places_bad_words before insert or update on places for each row execute function block_bad_words('name');
drop trigger if exists posts_bad_words on posts;
create trigger posts_bad_words before insert or update on posts for each row execute function block_bad_words('caption', 'cat_name');
