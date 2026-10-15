"""Native-resolution drawing primitives for the configurable silent Reel harness."""
from __future__ import annotations

import math
from pathlib import Path
import subprocess

from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps

from render_carousel import require


def ease(value):
    return 1 - (1 - max(0, min(1, value))) ** 3


class MediaFrames:
    """Decode a selected local clip sequentially, with no audio or remote fetch."""
    def __init__(self, media, size, fps, ffmpeg):
        self.media, self.size, self.fps, self.ffmpeg = media, size, fps, ffmpeg
        self.process, self.last, self.index = None, None, -1
        if media['kind'] == 'image':
            with Image.open(media['_path']) as original:
                self.last = ImageOps.exif_transpose(original).convert('RGB').copy()

    def frame(self, n):
        if self.media['kind'] == 'image':
            return self.last
        if n < self.index:
            self.close()
            self.index, self.last = -1, None
        if self.process is None:
            w, h = self.size
            cmd = [self.ffmpeg, '-v', 'error', '-threads', '1', '-ss', str(self.media.get('start', 0)),
                   '-i', str(self.media['_path']), '-t', str(self.media['_seconds']),
                   '-map', '0:v:0', '-an', '-sn', '-vf', f'fps={self.fps},scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black',
                   '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-']
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        while self.index < n:
            data = self.process.stdout.read(self.size[0] * self.size[1] * 3)
            if not data:
                require(self.last is not None, 'Could not decode the selected source clip.')
                require(self.process.wait() == 0, 'Source video decoder failed.')
                return self.last
            require(len(data) == self.size[0] * self.size[1] * 3, 'Source video ended in an incomplete frame.')
            self.last = Image.frombytes('RGB', self.size, data)
            self.index += 1
        return self.last

    def close(self):
        if self.process:
            if self.process.poll() is None:
                self.process.terminate()
            self.process.communicate()
            self.process = None


class Renderer:
    def __init__(self, post, brief, fonts):
        self.post, self.brief, self.fonts = post, brief, fonts
        delivery = brief['deliverable']
        self.width, self.height = delivery['width'], delivery['height']
        self.scale = self.width / 1080
        margins = delivery['safe_area']
        self.safe = (1080*margins['left'], 1920*margins['top'], 1080*(1-margins['right']), 1920*(1-margins['bottom']))
        self.left, self.top, right, bottom = self.safe
        self.sw, self.sh = right-self.left, bottom-self.top
        self.type_scale = self.sw / 770
        self.bg, self.ink = (ImageColor.getrgb(brief['brand'][k]) for k in ('background', 'text'))
        self.panel, self.panel_ink = (255, 255, 255), (0, 0, 0)
        self.tiles, self.font_cache, self.glyphs, self.bounds = {}, {}, set(), {}
        self.section, self.scene_id = 'header', ''

    def x(self, f):
        return self.left + self.sw*f

    def y(self, f):
        return self.top + self.sh*f

    def coords(self, xy):
        if isinstance(xy[0], (tuple, list)):
            return [(round(x*self.scale), round(y*self.scale)) for x, y in xy]
        return tuple(round(v*self.scale) for v in xy)

    def box_check(self, box, label):
        l, t, r, b = box
        sl, st, sr, sb = self.safe
        require(l >= sl-.01 and t >= st-.01 and r <= sr+.01 and b <= sb+.01,
                f'{self.scene_id}: {label} exceeds the safe area: {box}. Shorten copy or adjust the layout.')
        limits = {'header': (0, .075), 'kicker': (.075, .13), 'title': (.13, .32),
                  'visual': (.33, .785), 'body': (.80, .925), 'credit': (.925, .966)}
        if self.section in limits:
            lo, hi = limits[self.section]
            require(t >= self.y(lo)-.01 and b <= self.y(hi)+.01,
                    f'{self.scene_id}: {label} exceeds its {self.section} region. Shorten or reflow the copy.')
        key = (self.scene_id, self.section)
        old = self.bounds.get(key, box)
        self.bounds[key] = [min(old[0],l),min(old[1],t),max(old[2],r),max(old[3],b)]

    def text(self, im, x, y, value, size=36, bold=True, color=None, center=False, alpha=1):
        color = color or self.ink
        px = max(1, round(size*self.type_scale*self.scale))
        key = (value, px, bold, color)
        if key not in self.tiles:
            fk = (px, bold)
            if fk not in self.font_cache:
                self.font_cache[fk] = ImageFont.truetype(str(self.fonts['bold' if bold else 'regular']), px)
            f = self.font_cache[fk]
            for ch in set(value)-set(' \n\t\r'):
                if (ch,bold) not in self.glyphs:
                    mask, missing = f.getmask(ch), f.getmask('\U0010ffff')
                    require((mask.size, bytes(mask)) != (missing.size, bytes(missing)), f'Font is missing {ch!r}.')
                    self.glyphs.add((ch,bold))
            bb = f.getbbox(value, anchor='lt')
            padding = max(1, round(2*self.scale))
            tile = Image.new('RGBA',(math.ceil(f.getlength(value))+padding,bb[3]+padding))
            ImageDraw.Draw(tile).text((0,0),value,font=f,fill=color,anchor='lt')
            self.tiles[key] = tile
        tile = self.tiles[key]
        w,h = tile.width/self.scale, tile.height/self.scale
        if center:
            x -= w/2
        self.box_check((x,y,x+w,y+h),repr(value))
        if alpha < .999:
            tile = tile.copy()
            tile.putalpha(tile.getchannel('A').point(lambda a: round(a*max(0,min(1,alpha)))))
        im.paste(tile,(round(x*self.scale),round(y*self.scale)),tile)

    def line(self, d, points, width=3, fill=None):
        d.line(self.coords(points),fill=fill or self.ink,width=max(1,round(width*self.type_scale*self.scale)))

    def rect(self, d, box, fill=None, radius=0, width=3):
        self.box_check(box,'graphic')
        d.rounded_rectangle(self.coords(box),round(radius*self.scale),fill=fill or self.panel,outline=self.ink,width=max(1,round(width*self.scale)))

    def circle(self, d, x, y, radius, fill=None, width=3):
        self.box_check((x-radius,y-radius,x+radius,y+radius),'circle')
        d.ellipse(self.coords((x-radius,y-radius,x+radius,y+radius)),fill=fill or self.panel,outline=self.ink,width=max(1,round(width*self.scale)))

    def packet(self, d, p1, p2, t, phase=0, speed=.6, radius=6):
        p=(t*speed+phase)%1
        self.circle(d,p1[0]+(p2[0]-p1[0])*p,p1[1]+(p2[1]-p1[1])*p,radius*self.type_scale,self.ink,1)

    def frame(self, index, n, media=None):
        scene=self.post['scenes'][index]
        fps=self.brief['deliverable']['fps']
        t=n/fps
        self.scene_id=scene['id']
        im=Image.new('RGB',(self.width,self.height),self.bg)
        d=ImageDraw.Draw(im)
        self.section='header'
        self.text(im,self.x(.02),self.y(.018),self.brief['account']['display_name'],30)
        if self.post.get('demo'):
            self.text(im,self.x(.73),self.y(.025),'LAYOUT DEMO',15)
        self.line(d,(self.x(.02),self.y(.062),self.x(.98),self.y(.062)),2)
        self.section='kicker'
        self.text(im,self.x(.02),self.y(.09),scene.get('kicker',''),27)
        self.section='title'
        for j,value in enumerate(scene['title']):
            p=1 if index==0 else ease((t-j*.08)/.4)
            self.text(im,self.x(.02),self.y(.145+j*.087)+(1-p)*10,value,86,alpha=p)
        self.section='visual'
        self.visual(im,d,scene,t,n,media)
        self.section='body'
        self.line(d,(self.x(.02),self.y(.808),self.x(.98),self.y(.808)),2)
        for j,value in enumerate(scene['body']):
            self.text(im,self.x(.02),self.y(.827+j*.047),value,36)
        self.section='credit'
        self.text(im,self.x(.02),self.y(.94),scene['credit'],22,bold=False)
        self.section='progress'
        progress=(scene['_start']+t)/self.brief['deliverable']['duration_seconds']
        self.line(d,(self.x(.02),self.y(.98),self.x(.98),self.y(.98)),1)
        self.line(d,(self.x(.02),self.y(.98),self.x(.02+.96*progress),self.y(.98)),5)
        return im

    def media_size(self):
        # Fixed 16:9 window; each source is contained with its geometry preserved.
        width=round(self.sw*.96*self.scale)//2*2
        return width, round(width*9/16)//2*2

    def visual(self, im, d, scene, t, n, media):
        kind, data = scene['layout'], scene.get('visual',{})
        if kind=='media':
            frame=media.frame(n)
            size=self.media_size()
            frame=ImageOps.contain(frame,size,Image.Resampling.LANCZOS)
            box=(self.x(.02),self.y(.35),self.x(.02)+size[0]/self.scale,self.y(.35)+size[1]/self.scale)
            self.box_check(box,'media')
            x=round(box[0]*self.scale)+(size[0]-frame.width)//2
            y=round(box[1]*self.scale)+(size[1]-frame.height)//2
            im.paste(frame,(x,y))
            self.text(im,self.x(.5),self.y(.745),data.get('label',''),30,center=True)
        elif kind=='flow':
            nodes=data['nodes']
            points=[(.23,.40),(.77,.40),(.14,.70),(.50,.70),(.86,.70)][:len(nodes)]
            if len(nodes)<=3:
                points=[(.16+i*.68/(len(nodes)-1),.42) for i in range(len(nodes))]
            core=(self.x(.5),self.y(.565))
            for j,(node,(fx,fy)) in enumerate(zip(nodes,points)):
                x,y=self.x(fx),self.y(fy)
                self.line(d,(x,y,*core),2)
                for z in range(2):
                    self.packet(d,(x,y),core,t,j*.13+z*.5)
                pulse=3*math.sin(t*3-j)
                self.circle(d,x,y,(42+pulse)*self.type_scale)
                self.text(im,x,y-18*self.type_scale,node['symbol'],34,center=True,color=self.panel_ink)
                self.text(im,x,y+57*self.type_scale,node['label'],28,center=True)
            self.rect(d,(self.x(.285),self.y(.515),self.x(.715),self.y(.615)),radius=12)
            for j,label in enumerate(data['center']):
                self.text(im,core[0],self.y(.532+j*.041),label,31,center=True,color=self.panel_ink)
        elif kind=='steps':
            items=data['items']
            count=len(items)
            xs=[self.x(.14+j*.72/(count-1)) for j in range(count)]
            y=self.y(.595)
            r=52*self.type_scale
            for j,(x,item) in enumerate(zip(xs,items)):
                if j<count-1:
                    self.line(d,(x+r+3,y,xs[j+1]-r-3,y),3)
                    self.packet(d,(x+r+3,y),(xs[j+1]-r-3,y),t,j*.2,radius=5)
                self.circle(d,x,y,r)
                self.text(im,x,y-21*self.type_scale,item['symbol'],38,center=True,color=self.panel_ink)
                self.text(im,x,self.y(.68),item['label'],29,center=True)
            phase=max(0,min(count-1,(t-.4)/max(.1,scene['duration']-.9)*(count-1)))
            a=min(count-2,int(phase)); p=phase-a
            x=xs[a]+(xs[a+1]-xs[a])*ease(p)
            yy=self.y(.49)-self.sh*.075*math.sin(math.pi*p)
            self.circle(d,x,yy,29*self.type_scale,self.ink)
            self.text(im,x,yy-12*self.type_scale,data.get('token','+'),24,center=True,color=self.bg)
            self.text(im,self.x(.5),self.y(.748),data.get('note',''),27,center=True)
        elif kind=='occlusion':
            bx,by=self.x(.29),self.y(.65)
            self.line(d,(self.x(.05),self.y(.69),self.x(.95),self.y(.69)),3)
            self.circle(d,bx,by,22*self.type_scale,self.ink)
            p=t/scene['duration']
            cover=ease((p-.10)/.23) if p<.70 else 1-ease((p-.70)/.24)
            xx=self.x(.79)-(self.x(.79)-bx)*cover
            rw=self.sw*.093
            self.rect(d,(xx-rw,self.y(.51),xx+rw,self.y(.685)))
            self.text(im,xx,self.y(.565),data['cover_label'],30,center=True,color=self.panel_ink)
            if cover>.9:
                for angle in range(0,360,60):
                    d.arc(self.coords((bx-22*self.type_scale,by-22*self.type_scale,bx+22*self.type_scale,by+22*self.type_scale)),angle+t*30,angle+32+t*30,fill=self.panel_ink,width=max(1,round(3*self.scale)))
                self.line(d,(bx,by,self.x(.67),self.y(.43)),2)
                self.packet(d,(bx,by),(self.x(.67),self.y(.43)),t)
                self.text(im,self.x(.68),self.y(.375),data['memory_label'],32,center=True)
            self.text(im,self.x(.5),self.y(.74),data.get('note',''),29,center=True)
        elif kind=='cards':
            for j,item in enumerate(data['items']):
                top=.345+j*.139
                p=ease((t-j*.5)/.5)
                self.rect(d,(self.x(.02),self.y(top),self.x(.98),self.y(top+.12)))
                self.text(im,self.x(.10),self.y(top+.025)+3*math.sin(t*3-j),item['symbol'],38,color=self.panel_ink)
                self.text(im,self.x(.23),self.y(top+.017),item['label'],39,color=self.panel_ink,alpha=p)
                self.text(im,self.x(.23),self.y(top+.073),item['detail'],28,bold=False,color=self.panel_ink,alpha=p)
                self.line(d,(self.x(.03),self.y(top+.114),self.x(.03+.94*p),self.y(top+.114)),4,self.bg)
        elif kind=='metric':
            p=ease(t/.45)
            self.text(im,self.x(.02),self.y(.365)+(1-p)*20,data['value'],150,alpha=p)
            self.text(im,self.x(.02),self.y(.565),data['label'],43)
            self.rect(d,(self.x(.02),self.y(.665),self.x(.98),self.y(.765)))
            self.text(im,self.x(.5),self.y(.69),data['note'],33,center=True,color=self.panel_ink)
            # An orbit emphasizes the value without counting through false statistics.
            x=self.x(.83)+self.sw*.06*math.cos(t*2)
            y=self.y(.43)+self.sh*.035*math.sin(t*2)
            self.circle(d,x,y,10*self.type_scale,self.ink)


def encode_scene(renderer, index, folder, ffmpeg, media=None):
    scene=renderer.post['scenes'][index]
    fps=renderer.brief['deliverable']['fps']
    dest=folder/f'{index:02d}.mp4'
    size=f'{renderer.width}x{renderer.height}'
    cmd=[ffmpeg,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',size,'-r',str(fps),'-i','-',
         '-an','-vf','scale=out_color_matrix=bt709:out_range=tv','-c:v','libx264','-preset','veryfast','-crf','18',
         '-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)]
    # A file avoids encoder-error pipe deadlocks on malformed or failed encodes.
    with (folder/f'{index:02d}.log').open('wb+') as errors:
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=errors)
        try:
            for n in range(scene['_frames']):
                proc.stdin.write(renderer.frame(index,n,media).tobytes())
            proc.stdin.close()
            code=proc.wait()
            errors.seek(0)
            require(code==0, f'Encoder failed: {errors.read().decode(errors="replace")[-1500:]}')
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
            if not proc.stdin.closed:
                try:
                    proc.stdin.close()
                except BrokenPipeError:
                    pass
            if media:
                media.close()
    return dest
