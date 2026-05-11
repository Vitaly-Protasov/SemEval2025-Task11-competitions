# Official BRIGHTER Test Data

This folder was generated from the official Hugging Face dataset
`brighter-dataset/BRIGHTER-emotion-categories`.

Files in `test/` contain the test split for each official language
configuration, exported as CSV with the Track A-style columns:
`id,text,anger,fear,joy,sadness,surprise`.

Notes:
- The official dataset also contains a `disgust` label, which is not exported here.
- If the API returns a missing value for one of the exported emotion columns,
  it has been normalized to `0` in these CSVs.
- This data is kept separate from the Codabench reference set because the
  official BRIGHTER IDs/language inventory do not align 1:1 with the current bundle.

Generated configs:
afr, arq, ary, chn, deu, eng, esp, hau, hin, ibo, ind, jav, kin, mar, pcm, ptbr, ptmz, ron, rus, sun, swa, swe, tat, ukr, vmw, xho, yor, zul
