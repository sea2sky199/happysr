"""
Runs all SmithCase chapter scripts, saves figures to output/.
Uses Agg backend (no display needed) and suppresses animation delays.
"""
import sys
import os
import traceback
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Suppress animation pauses so plots run at full speed
plt.pause = lambda x: None

sys.path.insert(0, os.path.dirname(__file__))

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

_fig_counters = {}
_current_script = None

_orig_show = plt.show

def _patched_show(*args, **kwargs):
    prefix = _current_script or 'unknown'
    _fig_counters[prefix] = _fig_counters.get(prefix, 0) + 1
    figs = [plt.figure(n) for n in plt.get_fignums()]
    for fig in figs:
        fname = f'{prefix}_fig{_fig_counters[prefix]:02d}.png'
        fpath = os.path.join(OUTPUT_DIR, fname)
        fig.savefig(fpath, dpi=100, bbox_inches='tight')
        print(f'    saved {fname}')

plt.show = _patched_show

CHAPTERS = [
    'SmithCase_Chapter11',
    'SmithCase_Chapter12',
    'SmithCase_Chapter13',
    'SmithCase_Chapter14',
    'SmithCase_Chapter15',
    'SmithCase_Chapter16',
    'SmithCase_Chapter17',
    'SmithCase_Chapter18',
    'SmithCase_Chapter19',
    'SmithCase_Chapter20_LBS',
    'SmithCase_Chapter20_DFA',
    'SmithCase_Chapter20_FAP',
]

results = []

for chapter in CHAPTERS:
    _current_script = chapter
    script_path = os.path.join(os.path.dirname(__file__), chapter + '.py')
    print(f'\n--- {chapter} ---')
    t0 = time.time()
    try:
        # Each script runs in a fresh globals dict so module-level state is isolated
        glb = {'__name__': '__main__', '__file__': script_path}
        with open(script_path) as f:
            code = compile(f.read(), script_path, 'exec')
        exec(code, glb)
        elapsed = time.time() - t0
        plt.close('all')
        print(f'  OK  ({elapsed:.1f}s)')
        results.append((chapter, True, elapsed, None))
    except Exception as e:
        elapsed = time.time() - t0
        plt.close('all')
        tb = traceback.format_exc()
        print(f'  FAIL ({elapsed:.1f}s)\n{tb}')
        results.append((chapter, False, elapsed, tb))

print('\n' + '='*60)
print(f'{"Chapter":<35} {"Status":>6}  {"Time":>6}')
print('-'*60)
for chapter, ok, elapsed, _ in results:
    status = 'OK' if ok else 'FAIL'
    print(f'{chapter:<35} {status:>6}  {elapsed:>5.1f}s')

total = len(results)
passed = sum(1 for _, ok, _, _ in results if ok)
print(f'\n{passed}/{total} chapters passed')
print(f'Figures saved to: {OUTPUT_DIR}')
