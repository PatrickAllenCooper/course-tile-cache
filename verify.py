"""Reproduce all saved scores without network access or a model account."""
from pathlib import Path
import json
import subprocess
import sys
from check_example import check

def score(path, dev=False):
    cmd=[sys.executable, 'score.py', str(path)] + (['--dev'] if dev else [])
    proc=subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    data=json.loads(proc.stdout)
    assert proc.returncode == (0 if data['passed'] else 1)
    return data

if __name__ == '__main__':
    record=json.loads(Path('research/results.json').read_text())
    check()
    assert score('baseline.py')==record['baseline']
    for row in record['trials']:
        file=Path('runs',row['run'],'candidate.py')
        assert score(file,True)==row['development'],row['run']
        assert score(file)==row['final'],row['run']
    assert Path('candidate.py').read_bytes()==Path('runs',record['selected'],'candidate.py').read_bytes()
    assert score('candidate.py')==record['result']
    print('Reproduced starting policy, six paired-condition entries and selected result.')
    print('Selected candidate meets the frozen target:',record['result']['passed'])
