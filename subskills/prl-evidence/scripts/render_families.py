#!/usr/bin/env python3
"""Render original synthetic physics-figure demonstrations, never research results."""
import argparse
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image,ImageDraw
from corpus_lib import write_json,sha256
from coverage_catalog import families
from prl_figure import figure_context,export_figure
from figure_recipes import build,implemented
ROOT=Path(__file__).resolve().parents[1]


def render(names,out,grayscale=False,seed=20261016):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);catalog=families();rows=[]
    for name in names:
        if name not in catalog or name not in implemented():raise ValueError('unimplemented family: '+name)
        with figure_context():
            example=build(name,seed);data_path=out/(name+'.npz');np.savez(data_path,**example.data)
            provenance={'data_kind':'original_synthetic_demonstration','family':name,'seed':seed,'data_file':data_path.name,'data_sha256':sha256(data_path),'transformations':example.transformations,'scientific_claim':'No empirical finding; layout demonstration only.','caption':example.caption,
                        'recipe_source_sha256':{str(p.relative_to(ROOT)):sha256(p) for p in sorted((ROOT/'scripts/figure_recipes').glob('*.py'))}}
            report=export_figure(example.figure,out/name,provenance,grayscale=grayscale);plt.close(example.figure)
        (out/(name+'.caption.txt')).write_text('SYNTHETIC DEMONSTRATION. '+example.caption+'\n')
        rows.append({'family':name,'passed':report['passed'],'errors':report['artist_inspection']['errors'],'warnings':report['artist_inspection']['warnings'],'pdf':name+'.pdf','png':name+'.png','report':name+'.json'})
    for start in range(0,len(rows),12):
        subset=rows[start:start+12];sheet=Image.new('RGB',(1500,390*((len(subset)+2)//3)),'white');draw=ImageDraw.Draw(sheet)
        for i,row in enumerate(subset):
            with Image.open(out/row['png']) as im:thumb=im.convert('RGB');thumb.thumbnail((490,355))
            x=(i%3)*500;y=(i//3)*390;sheet.paste(thumb,(x+(500-thumb.width)//2,y+25));draw.text((x+10,y+5),row['family'],fill='black')
        sheet.save(out/f'preview-{start//12+1}.jpg',quality=92)
    summary={'passed':all(r['passed'] for r in rows),'figures':rows,'count':len(rows),'grayscale_requested':grayscale,'visual_review':'pending','data_kind':'original_synthetic_demonstration','artifact_sha256':{p.name:sha256(p) for p in sorted(out.iterdir()) if p.is_file() and p.suffix in ['.pdf','.png','.npz','.txt','.jpg']}}
    write_json(out/'families-report.json',summary)
    return summary


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--family',choices=sorted(implemented()));g.add_argument('--all',action='store_true');p.add_argument('--output',type=Path,required=True);p.add_argument('--grayscale',action='store_true');a=p.parse_args()
    r=render(sorted(implemented()) if a.all else [a.family],a.output,a.grayscale)
    print(json.dumps({'passed':r['passed'],'count':r['count'],'failures':[x for x in r['figures'] if not x['passed']]},indent=2));raise SystemExit(0 if r['passed'] else 1)
