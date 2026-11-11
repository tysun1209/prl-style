#!/usr/bin/env python3
"""Synthetic API demonstration: distinct diffusivities can have equal values."""
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from prl_figure import figure_context,new_figure,export_figure
from quantity_audit import load_artifacts
from validate_claims import validate
from corpus_lib import write_json


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    ledger=json.loads((ROOT/'assets/templates/claim-ledger.json').read_text())
    ledger['evidence']=[dict(id='E1',kind='synthetic_demo',source=__file__,locator='main: two distinct coefficients equal to one',description='Invented API example; no research inference.')]
    ledger['claims']=[dict(id='C1',text='Two distinct quantities have value one in this synthetic fixture.',scope='Synthetic fixture only',strength='definition',uncertainty='not measured',status='supported',evidence_ids=['E1'],figure_ids=['F'],citation_ids=[],protected_facts=[dict(id='values',meaning='separate tracer and field coefficients',value='1',unit='arbitrary diffusivity unit')])]
    ledger['figures']=[{'id':'F'}]
    definitions=[('tracer','bare tracer diffusivity','D_y'),('field','field diffusivity','D_0'),('effective','effective tracer diffusivity','D_eff')]
    ledger['quantities']=[dict(id=q,meaning=m,source_symbol=s,unit='arbitrary diffusivity unit',scope='synthetic-model',evidence_id='E1',source_locator='main: definitions',value=1) for q,m,s in definitions]
    ledger['quantity_usages']=[dict(quantity_id=q,symbol=s,artifact_id='F',locator='axes[0].ylabel') for q,s in [('effective','D_eff'),('tracer','D_y')]]+[dict(quantity_id=q,symbol=s,artifact_id='captions',locator='text') for q,m,s in definitions]
    (args.output/'captions.txt').write_text('Synthetic demonstration. D_eff is the effective tracer diffusivity; D_y is the bare tracer diffusivity; D_0 is the distinct field diffusivity. Each is set to one in arbitrary units.\n虚构示例。D_eff 为有效示踪扩散系数，D_y 为裸示踪扩散系数，D_0 为另一个场扩散系数；三者均取任意单位下的数值 1。\n')
    with figure_context():
        fig,ax=new_figure();ax.plot([0,1],[1,1],marker='o');ax.set(xlabel='Dimensionless time',ylabel=r'$D_{\mathrm{eff}}/D_y$');export_figure(fig,args.output/'figure',{'kind':'synthetic_demo'});plt.close(fig)
    write_json(args.output/'ledger.json',ledger)
    artifacts,provenance=load_artifacts([f'F={args.output}/figure.json'],[f'captions={args.output}/captions.txt'])
    result=validate(ledger,artifacts);result['audited_artifacts']=provenance;write_json(args.output/'audit.json',result)
    if not result['passed']:raise SystemExit(1)


if __name__=='__main__':main()
