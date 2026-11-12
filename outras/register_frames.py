from pathlib import Path
import json, statistics
from PIL import Image
root=Path('/private/tmp/nina-orange/run/qa/frames')
reports=[]
# A shared transform per state preserves every generated pose and vertical displacement.
# Match resting states to the source jump's resting size, reserving room for its lift.
jump=Image.open(root/'jumping/04.png').convert('RGBA')
jb=jump.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox()
target_height=jb[3]-jb[1]
for folder in sorted(p for p in root.iterdir() if p.is_dir()):
    files=sorted(folder.glob('*.png'))
    ims=[Image.open(p).convert('RGBA') for p in files]
    boxes=[im.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox() for im in ims]
    refheight=(boxes[-1][3]-boxes[-1][1]) if folder.name=='jumping' else max(b[3]-b[1] for b in boxes)
    scale=min(1,target_height/refheight)
    ground=max(b[3] for b in boxes)
    dy=203-round(ground*scale)
    for p,im in zip(files,ims):
        resized=im.resize((round(192*scale),round(208*scale)),Image.Resampling.LANCZOS)
        canvas=Image.new('RGBA',(192,208))
        canvas.alpha_composite(resized,((192-resized.width)//2,dy))
        canvas.save(p)
    reports.append({'state':folder.name,'scale':scale,'ground_shift':dy,'reference_height':refheight,'target_height':target_height})
(root.parent/'registration.json').write_text(json.dumps({'transforms':reports},indent=2))
