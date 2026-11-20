"""Collect bounded, fresh model calls. Run with 'python3 research/trials.py OUTPUT_DIR'.
Run scoring separately after reviewing all returned code. Never overwrite a run."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import time

MODEL = 'gpt-6.1-sol'


def ask(folder, prompt):
    folder.mkdir(parents=True,exist_ok=False)
    (folder/'prompt.txt').write_text(prompt)
    started=time.monotonic()
    with tempfile.TemporaryDirectory() as tmp:
        cmd=['codex','exec','--ignore-user-config','--ignore-rules','--ephemeral',
             '--skip-git-repo-check','-C',tmp,'-s','read-only','--json','-m',MODEL,
             '--disable','shell_tool','--disable','apps','--disable','multi_agent',
             '--disable','skill_search','--enable','skip_host_skill_discovery',
             '-c','web_search="disabled"','-c','model_reasoning_effort="low"',
             '-o',str(Path(tmp)/'reply'),'-']
        try:
            proc = subprocess.run(cmd,input=prompt,text=True,capture_output=True,timeout=100,cwd=tmp)
            events=[json.loads(x) for x in proc.stdout.splitlines() if x.startswith('{')]
            usage=[e.get('usage') for e in events if e.get('usage')]
            content=Path(tmp,'reply').read_text() if Path(tmp,'reply').exists() else ''
            status='ok' if proc.returncode==0 and content.strip() else 'unavailable'
            if status!='ok': print(proc.stderr[-800:],events[-2:],flush=True)
        except subprocess.TimeoutExpired:
            content='';usage=[];status='timeout'
    (folder/'reply.txt').write_text(content)
    record=dict(model=MODEL,backend='Codex CLI',effort='low',seconds=round(time.monotonic()-started,2),
                status=status,usage=usage,cost=None,prompt_file='prompt.txt')
    (folder/'call.json').write_text(json.dumps(record,indent=2)+'\n')
    print(folder.name,status,record['seconds'],flush=True)
    return content


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('output',type=Path)
    args=cli.parse_args()
    root=Path(__file__).resolve().parents[1]
    task=(root/'brain/objective.md').read_text()
    source=(root/'baseline.py').read_text()
    context=task+'\nStarting implementation\n'+source
    plan=ask(args.output/'00-plan',context+'\nPlan only. In at most 130 words identify the user constraint, one design hypothesis, an edge case and a stopping check. No code. No tools. No questions.')
    if not plan: raise SystemExit('Planning backend unavailable; stopped before trials.')
    for pair in range(1,4):
        for condition in ('plain','assisted'):
            name=f'{pair:02}-{condition}'
            prompt=context
            if condition=='assisted':prompt+='\nSaved planning note\n'+plan
            prompt+='\nReturn only a complete Python module implementing this function. Use standard library only. No tools, external files, persistent state or prose. The evaluator will import the module.'
            folder=args.output/name
            reply=ask(folder,prompt).strip()
            if reply.startswith('```') and reply.endswith('```'): reply='\n'.join(reply.splitlines()[1:-1])
            if reply: (folder/'candidate.py').write_text(reply+'\n')
if __name__=='__main__':main()
