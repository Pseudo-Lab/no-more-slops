# Pawstamp 캐릭터 생성 프롬프트

ChatGPT(이미지 생성)나 Midjourney로 27종을 **같은 그림체**로 뽑기 위한 프롬프트.

## 진행 순서

1. **기준 그림 1장부터**: 아래 공통 프롬프트에 `말티즈` 설명을 넣어 생성한다. 마음에 들 때까지 다시 뽑는다. 이 그림이 전체 그림체의 기준이 된다.
2. **같은 대화창에서 이어서**: "방금 그림과 **완전히 같은 스타일, 같은 구도, 같은 크기**로 [견종 설명]으로 바꿔줘"라고 하나씩 요청한다. 새 대화창을 열면 그림체가 달라진다.
   - Midjourney라면 기준 그림을 `--sref`(스타일 참조)로 넣는다.
3. **배경은 투명**으로 받는다(PNG). 앱에서 견종별 파스텔 원형 배경을 따로 깔기 때문.
4. **파일 이름**을 아래 표의 영문 이름으로 저장한다. 예: `maltese.png`
5. `~/Desktop/share/pawstamp-characters/` 폴더에 넣고 Claude에게 "넣었어"라고 말하면, 크기를 줄여서 앱에 반영한다. 일부만 넣어도 되고, 없는 건 지금 캐릭터가 그대로 나온다.

## 공통 프롬프트 (영어가 결과가 더 안정적)

```
A cute front-facing head portrait of [DESCRIPTION], centered, looking straight at the viewer with a gentle happy expression.
Modern flat vector illustration with soft gradient shading, rounded simple shapes, clean smooth edges, no outlines.
Big glossy dark eyes with small white highlights, small nose, subtle pink blush on the cheeks.
Head and a little bit of the neck only, the head fills about 80% of the square frame.
Transparent background, no text, no shadow, no props, no clothes.
Part of a consistent character icon set for a pet app. Square 1024x1024.
```

> 고양이는 첫 문장의 끝에 `, a Korean street cat`을 붙이고 `small pink nose and thin whiskers`를 더한다.

## 견종별 [DESCRIPTION]

| 이름 | 파일 이름 | DESCRIPTION |
|---|---|---|
| 말티즈 (기준) | `maltese` | a fluffy pure white Maltese dog with long silky hanging ears and a tuft of hair on top of the head |
| 푸들 | `poodle` | an apricot brown toy poodle with curly fur, round fluffy curly ears and a pom-pom top knot |
| 포메라니안 | `pomeranian` | an orange Pomeranian with a big fluffy round mane, tiny pointy ears and a fox-like little face |
| 시츄 | `shihtzu` | a white and light-brown Shih Tzu with long hanging brown ears, brown patches around the eyes and a small pink bow on the top knot |
| 비숑 프리제 | `bichon` | a pure white Bichon Frise with a perfectly round cloud-like fluffy head |
| 치와와 | `chihuahua` | a fawn tan Chihuahua with very large upright ears and a small apple-shaped head |
| 웰시코기 | `corgi` | an orange and white Welsh Corgi with big upright pointy ears, white muzzle and a white stripe on the forehead, tongue slightly out |
| 진돗개 | `jindo` | a cream white Korean Jindo dog with upright triangle ears and a calm gentle face |
| 시바견 | `shiba` | a red Shiba Inu with cream white cheeks and eyebrow dots, small upright triangle ears |
| 골든 리트리버 | `golden` | a golden retriever with warm golden fur, soft floppy ears and a friendly smile with tongue slightly out |
| 래브라도 리트리버 | `labrador` | a light yellow Labrador retriever with short smooth fur and soft floppy ears |
| 닥스훈트 | `dachshund` | a red-brown Dachshund with long floppy ears and a slightly long snout |
| 요크셔테리어 | `yorkie` | a Yorkshire terrier with tan face, steel blue-gray hair on top of the head, small pointy ears and a tiny pink bow |
| 프렌치 불독 | `frenchie` | a cream fawn French Bulldog with big rounded bat ears, a flat dark muzzle and soft forehead wrinkles |
| 보스턴테리어 | `boston` | a black and white Boston Terrier with big bat ears, a white stripe between the eyes and a white muzzle |
| 퍼그 | `pug` | a fawn pug with a black flat face mask, small black folded ears and soft wrinkles |
| 비글 | `beagle` | a tricolor beagle with brown head, long brown floppy ears, white stripe on the forehead and white muzzle |
| 보더콜리 | `bordercollie` | a black and white Border Collie with semi-folded ears, white blaze and white muzzle, tongue slightly out |
| 미니어처 슈나우저 | `schnauzer` | a salt-and-pepper gray miniature Schnauzer with white bushy eyebrows, a white beard and folded ears |
| 말티푸 | `maltipoo` | a cream apricot Maltipoo with soft curly fur and curly floppy ears |
| 사모예드 | `samoyed` | a fluffy pure white Samoyed with upright pointy ears, a big fluffy mane and a wide smile with tongue out |
| 기타·믹스 | `mixed` | a mixed-breed light brown dog with medium floppy ears and a friendly ordinary look |
| 치즈 (고양이) | `cat-cheese` | an orange tabby cat with darker orange stripes on the forehead and cheeks |
| 고등어 (고양이) | `cat-mackerel` | a gray mackerel tabby cat with dark gray stripes on the forehead and cheeks |
| 삼색이 (고양이) | `cat-calico` | a calico cat, mostly white face with an orange patch on one ear and a black patch on the other ear |
| 턱시도 (고양이) | `cat-tuxedo` | a black and white tuxedo cat with a black head, white muzzle and a white stripe down the nose |
| 까망이 (고양이) | `cat-black` | a black cat with round yellow eyes |

## 팁

- 그림체가 계속 어긋나면 "이전 그림의 눈 크기, 볼 터치, 그림자 방식을 그대로 유지해줘"라고 짚어준다.
- 너무 유아틱하면 `cute`를 `charming`으로 바꾸고 `minimal`을 추가한다.
- 상업적으로 쓸 예정이면 사용하는 이미지 생성 서비스의 상업 이용 조건을 확인한다.
