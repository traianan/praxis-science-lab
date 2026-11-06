import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from build_redirects import build, redirect_html
from seo import ROOT


class RedirectTests(unittest.TestCase):
    def test_paths_queries_fragments_and_fixed_origin(self):
        cases = [
            ('/praxis-science-lab/', '', '', 'https://praxissciencelab.app/'),
            ('/praxis-science-lab', '', '', 'https://praxissciencelab.app/'),
            ('/praxis-science-lab/apps/tempolab/privacy/ro.html', '?from=old', '#data', 'https://praxissciencelab.app/apps/tempolab/privacy/ro.html?from=old#data'),
            ('/praxis-science-lab/unknown/path', '', '', 'https://praxissciencelab.app/unknown/path'),
            ('/praxis-science-lab//example.com', '?url=https://other.invalid', '', 'https://praxissciencelab.app/example.com?url=https://other.invalid'),
        ]
        harness = '''const vm=require('node:vm'),fs=require('node:fs');
const source=fs.readFileSync(process.argv[1],'utf8');
const cases=JSON.parse(process.argv[2]);
for(const [pathname,search,hash,expected] of cases){
let actual; vm.runInNewContext(source,{window:{location:{pathname,search,hash,replace:u=>actual=u}}});
if(actual!==expected) throw new Error(JSON.stringify({actual,expected}));
}'''
        subprocess.run(['node', '-e', harness, str(ROOT/'scripts/legacy_redirect.js'), json.dumps(cases)], check=True, capture_output=True)

    def test_no_javascript_fallback(self):
        html = redirect_html('https://praxissciencelab.app/apps/tempolab/')
        self.assertIn('http-equiv="refresh" content="0;url=https://praxissciencelab.app/apps/tempolab/"', html)
        self.assertIn('rel="canonical" href="https://praxissciencelab.app/apps/tempolab/"', html)

    def test_artifact_contains_only_redirects(self):
        (ROOT/'build').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'build') as directory:
            output = build(Path(directory)/'redirects')
            files = list(output.rglob('*'))
            self.assertFalse((output/'pfa-studio').exists())
            self.assertFalse((output/'scripts').exists())
            self.assertFalse((output/'publishing/developer-profile').exists())
            self.assertTrue((output/'apps/auralis/privacy/ro.html').exists())
            for path in files:
                if path.is_file():
                    self.assertTrue(path.suffix == '.html' or path.name in {'redirect.js', '.nojekyll', 'robots.txt'})
                    if path.suffix == '.html':
                        self.assertIn('http-equiv="refresh"', path.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
