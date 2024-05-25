## Test 1
#### Input

###### sync_sql_blc_test.txt

```
INSERT INTO Plot (PlotId,  PlotInfo) VALUE('1','kl_clt_01');
INSERT INTO Plot (PlotId, PlotInfo) VALUE('2','kl_tvc_02');
INSERT INTO Plot (PlotId, PlotInfo) VALUE('3','dl_del_03');
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('101','81','1');
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('201','82','2');  
```

###### schema_dict.txt

```
{"khatauni": {"table_name": "khatauni", "columns": [], "col": [["KId", "varchar(255)"], ["Aadhar", "varchar(255)"], ["PId", "varchar(255)"]], "for_key_dep_on": ["PId -> plot.PlotId"], "pk": "KId"}, "plot": {"table_name": "plot", "columns": [], "col": [["PlotId", "varchar(255)"], ["PlotInfo", "varchar(255)"]], "for_key_dep_on": [], "pk": "PlotId"}}
```

#### Output

```

INSERT INTO Plot (PlotId,  PlotInfo) VALUE('1','kl_clt_01');
prev blc #: 0000000000000000000000000000000000000000000000000000000000000000
curr table#: 0xede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
transformed blc: createPlotEntry('1','kl_clt_01',True)
curr blc#: ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
hash match status: pass

*************

INSERT INTO Plot (PlotId, PlotInfo) VALUE('2','kl_tvc_02');
prev blc #: ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
curr table#: 0x5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
transformed blc: createPlotEntry('2','kl_tvc_02',True)
curr blc#: 5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
hash match status: pass

*************

INSERT INTO Plot (PlotId, PlotInfo) VALUE('3','dl_del_03');
prev blc #: 5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
curr table#: 0x046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
transformed blc: createPlotEntry('3','dl_del_03',True)
curr blc#: 046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
hash match status: pass

*************

INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('101','81','1');
prev blc #: 046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
curr table#: 0xbce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
transformed blc: createKhatauniEntry('101','81','1',True)
curr blc#: bce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
hash match status: pass

*************

INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('201','82','2');
prev blc #: bce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
curr table#: 0x9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
transformed blc: createKhatauniEntry('201','82','2',True)
curr blc#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
hash match status: pass

*************

```

## Test 2
Revert on purpose
#### Input

###### sync_sql_blc_test.txt

```
INSERT INTO Plot (PlotId,  PlotInfo) VALUE('1','kl_clt_01');
INSERT INTO Plot (PlotId, PlotInfo) VALUE('2','kl_tvc_02');
INSERT INTO Plot (PlotId, PlotInfo) VALUE('3','dl_del_03');
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('101','81','1');
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('201','82','2');  
```

###### schema_dict.txt

```
{"khatauni": {"table_name": "khatauni", "columns": [], "col": [["KId", "varchar(255)"], ["Aadhar", "varchar(255)"], ["PId", "varchar(255)"]], "for_key_dep_on": ["PId -> plot.PlotId"], "pk": "KId"}, "plot": {"table_name": "plot", "columns": [], "col": [["PlotId", "varchar(255)"], ["PlotInfo", "varchar(255)"]], "for_key_dep_on": [], "pk": "PlotId"}}
```

#### Output

```
Initial #check passed
INSERT INTO Plot (PlotId,  PlotInfo) VALUE('1','kl_clt_01');
prev blc #: 0000000000000000000000000000000000000000000000000000000000000000
curr table#: 0xede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
transformed blc: createPlotEntry('1','kl_clt_01',True)
revert func: deletePlotRecord('1',False)
curr blc#: ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
hash match status: pass

*************

Reverted
curr table#: 0000000000000000000000000000000000000000000000000000000000000000
curr blc#: 0000000000000000000000000000000000000000000000000000000000000000
Initial #check passed
INSERT INTO Plot (PlotId, PlotInfo) VALUE('2','kl_tvc_02');
prev blc #: 0000000000000000000000000000000000000000000000000000000000000000
curr table#: 0x971514d7caea59ce06f3c3862ef92298186c78a72db7cf7230b07ca5a493dfaf
transformed blc: createPlotEntry('2','kl_tvc_02',True)
revert func: deletePlotRecord('2',False)
curr blc#: 971514d7caea59ce06f3c3862ef92298186c78a72db7cf7230b07ca5a493dfaf
hash match status: pass

*************

Reverted
curr table#: 0000000000000000000000000000000000000000000000000000000000000000
curr blc#: 0000000000000000000000000000000000000000000000000000000000000000
Initial #check passed
INSERT INTO Plot (PlotId, PlotInfo) VALUE('3','dl_del_03');
prev blc #: 0000000000000000000000000000000000000000000000000000000000000000
curr table#: 0x6e382a6938ab3bf4dd0918e2e95e5bdc4b10cff7ae242fde93a2f18bd9bfbfe5
transformed blc: createPlotEntry('3','dl_del_03',True)
revert func: deletePlotRecord('3',False)
curr blc#: 6e382a6938ab3bf4dd0918e2e95e5bdc4b10cff7ae242fde93a2f18bd9bfbfe5
hash match status: pass

*************

Reverted
curr table#: 0000000000000000000000000000000000000000000000000000000000000000
curr blc#: 0000000000000000000000000000000000000000000000000000000000000000
Initial #check passed
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('101','81','1');
prev blc #: 0000000000000000000000000000000000000000000000000000000000000000
curr table#: 0xdf726d63c2de35cc88a31df8aab3db3e6076f0985a3562408ac9cbe6c9b3167a
transformed blc: createKhatauniEntry('101','81','1',True)
revert func: deleteKhatauniRecord('101',False)
curr blc#: df726d63c2de35cc88a31df8aab3db3e6076f0985a3562408ac9cbe6c9b3167a
hash match status: pass

*************

Reverted
curr table#: 0000000000000000000000000000000000000000000000000000000000000000
curr blc#: 0000000000000000000000000000000000000000000000000000000000000000
Initial #check passed
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('201','82','2');
prev blc #: 0000000000000000000000000000000000000000000000000000000000000000
curr table#: 0x51547030019e56381bdc4ecad6d424c520f2ef95a3b62dbb2ba7a23fdfa8854f
transformed blc: createKhatauniEntry('201','82','2',True)
revert func: deleteKhatauniRecord('201',False)
curr blc#: 51547030019e56381bdc4ecad6d424c520f2ef95a3b62dbb2ba7a23fdfa8854f
hash match status: pass

*************

Reverted
curr table#: 0000000000000000000000000000000000000000000000000000000000000000
curr blc#: 0000000000000000000000000000000000000000000000000000000000000000

```

## Test 3
#### Input

###### sync_sql_blc_test.txt

```
INSERT INTO Plot (PlotId,  PlotInfo) VALUE('1','kl_clt_01');
INSERT INTO Plot (PlotId, PlotInfo) VALUE('2','kl_tvc_02');
INSERT INTO Plot (PlotId, PlotInfo) VALUE('3','dl_del_03');
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('101','81','1');
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('201','82','2');  
DELETE FROM Khatauni WHERE KId = '101';
DELETE FROM Khatauni WHERE KId = '201';
DELETE FROM Plot WHERE PlotId = '1';
DELETE FROM Plot WHERE PlotId = '2';
DELETE FROM Plot WHERE PlotId = '3';
```

###### schema_dict.txt

```
{"khatauni": {"table_name": "khatauni", "columns": [], "col": [["KId", "varchar(255)"], ["Aadhar", "varchar(255)"], ["PId", "varchar(255)"]], "for_key_dep_on": ["PId -> plot.PlotId"], "pk": "KId"}, "plot": {"table_name": "plot", "columns": [], "col": [["PlotId", "varchar(255)"], ["PlotInfo", "varchar(255)"]], "for_key_dep_on": [], "pk": "PlotId"}}
```

#### Output

```
Initial #check passed
INSERT INTO Plot (PlotId,  PlotInfo) VALUE('1','kl_clt_01');
prev blc #: 0000000000000000000000000000000000000000000000000000000000000000
curr table#: 0xede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
transformed blc: createPlotEntry('1','kl_clt_01',True)
revert func: deletePlotRecord('1',False)
curr blc#: ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
hash match status: pass

*************

Initial #check passed
INSERT INTO Plot (PlotId, PlotInfo) VALUE('2','kl_tvc_02');
prev blc #: ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
curr table#: 0x5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
transformed blc: createPlotEntry('2','kl_tvc_02',True)
revert func: deletePlotRecord('2',False)
curr blc#: 5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
hash match status: pass

*************

Initial #check passed
INSERT INTO Plot (PlotId, PlotInfo) VALUE('3','dl_del_03');
prev blc #: 5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
curr table#: 0x046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
transformed blc: createPlotEntry('3','dl_del_03',True)
revert func: deletePlotRecord('3',False)
curr blc#: 046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
hash match status: pass

*************

Initial #check passed
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('101','81','1');
prev blc #: 046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
curr table#: 0xbce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
transformed blc: createKhatauniEntry('101','81','1',True)
revert func: deleteKhatauniRecord('101',False)
curr blc#: bce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
hash match status: pass

*************

Initial #check passed
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('201','82','2');
prev blc #: bce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
curr table#: 0x9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
transformed blc: createKhatauniEntry('201','82','2',True)
revert func: deleteKhatauniRecord('201',False)
curr blc#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
hash match status: pass

*************

Initial #check passed
DELETE FROM Khatauni WHERE KId = '101';
prev blc #: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr table#: 0xfbfc8804df0b8694e7fe8dab9e535f9a533381d12c2e6515dc3e728d6622eca5
transformed blc: deleteKhatauniRecord('101',True)
revert func: rollbackDeleteKhatauniRecord('101')
curr blc#: fbfc8804df0b8694e7fe8dab9e535f9a533381d12c2e6515dc3e728d6622eca5
hash match status: pass

*************

Initial #check passed
DELETE FROM Khatauni WHERE KId = '201';
prev blc #: fbfc8804df0b8694e7fe8dab9e535f9a533381d12c2e6515dc3e728d6622eca5
curr table#: 0x44f0043dba16d5f850a6eb1fa08e6c722fda2fe438f484dbde78df218bb274c7
transformed blc: deleteKhatauniRecord('201',True)
revert func: rollbackDeleteKhatauniRecord('201')
curr blc#: 44f0043dba16d5f850a6eb1fa08e6c722fda2fe438f484dbde78df218bb274c7
hash match status: pass

*************

Initial #check passed
DELETE FROM Plot WHERE PlotId = '1';
prev blc #: 44f0043dba16d5f850a6eb1fa08e6c722fda2fe438f484dbde78df218bb274c7
curr table#: 0x6fc3ad52c1c77489bf1e2aca9a3fae296ba23f920f589ead48af7c4681eaa0cb
transformed blc: deletePlotRecord('1',True)
revert func: rollbackDeletePlotRecord('1')
curr blc#: 6fc3ad52c1c77489bf1e2aca9a3fae296ba23f920f589ead48af7c4681eaa0cb
hash match status: pass

*************

Initial #check passed
DELETE FROM Plot WHERE PlotId = '2';
prev blc #: 6fc3ad52c1c77489bf1e2aca9a3fae296ba23f920f589ead48af7c4681eaa0cb
curr table#: 0x92de376f4333cc94e342eb97662b023239c5061b91693c271684febc38f1faf9
transformed blc: deletePlotRecord('2',True)
revert func: rollbackDeletePlotRecord('2')
curr blc#: 92de376f4333cc94e342eb97662b023239c5061b91693c271684febc38f1faf9
hash match status: pass

*************

Initial #check passed
DELETE FROM Plot WHERE PlotId = '3';
prev blc #: 92de376f4333cc94e342eb97662b023239c5061b91693c271684febc38f1faf9
curr table#: 0x5a80fe6ae96c2aa566bcd37cd04ef64ab6da6b9249bfd0e9b15e28612bf239a4
transformed blc: deletePlotRecord('3',True)
revert func: rollbackDeletePlotRecord('3')
curr blc#: 5a80fe6ae96c2aa566bcd37cd04ef64ab6da6b9249bfd0e9b15e28612bf239a4
hash match status: pass

*************
```

## Test 4
first ran insert records without revert
deleted and reverted delete khataunis
sat intial hash at 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69

```
Initial #check passed
DELETE FROM Khatauni WHERE KId = '101';
prev blc #: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr table#: 0xfbfc8804df0b8694e7fe8dab9e535f9a533381d12c2e6515dc3e728d6622eca5
transformed blc: deleteKhatauniRecord('101',True)
revert func: rollbackDeleteKhatauniRecord('101')
curr blc#: fbfc8804df0b8694e7fe8dab9e535f9a533381d12c2e6515dc3e728d6622eca5
hash match status: pass

*************

Reverted
curr table#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr blc#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
Initial #check passed
DELETE FROM Khatauni WHERE KId = '201';
prev blc #: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr table#: 0x54b36a220e2c3c8ead3983b57fbdb7922a589306f13c88e8358cdadefab81f06
transformed blc: deleteKhatauniRecord('201',True)
revert func: rollbackDeleteKhatauniRecord('201')
curr blc#: 54b36a220e2c3c8ead3983b57fbdb7922a589306f13c88e8358cdadefab81f06
hash match status: pass

*************

Reverted
curr table#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr blc#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69

```

## Test 5
first ran insert records, deleted khataunis without revert
deleted and reverted delete plots
sat intial hash at 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69

```
DELETE FROM Plot WHERE PlotId = '1';
prev blc #: 44f0043dba16d5f850a6eb1fa08e6c722fda2fe438f484dbde78df218bb274c7
curr table#: 0x6fc3ad52c1c77489bf1e2aca9a3fae296ba23f920f589ead48af7c4681eaa0cb
transformed blc: deletePlotRecord('1',True)
revert func: rollbackDeletePlotRecord('1')
curr blc#: 6fc3ad52c1c77489bf1e2aca9a3fae296ba23f920f589ead48af7c4681eaa0cb
hash match status: pass

*************

Reverted
curr table#: 44f0043dba16d5f850a6eb1fa08e6c722fda2fe438f484dbde78df218bb274c7
curr blc#: 44f0043dba16d5f850a6eb1fa08e6c722fda2fe438f484dbde78df218bb274c7
Initial #check passed
DELETE FROM Plot WHERE PlotId = '2';
prev blc #: 44f0043dba16d5f850a6eb1fa08e6c722fda2fe438f484dbde78df218bb274c7
curr table#: 0xafcb39c0ed33a08dc4291322c008c62de81fdd3b37cdb9e5f9af26d9e7de3b4c
transformed blc: deletePlotRecord('2',True)
revert func: rollbackDeletePlotRecord('2')
curr blc#: afcb39c0ed33a08dc4291322c008c62de81fdd3b37cdb9e5f9af26d9e7de3b4c
hash match status: pass

*************

Reverted
curr table#: 44f0043dba16d5f850a6eb1fa08e6c722fda2fe438f484dbde78df218bb274c7
curr blc#: 44f0043dba16d5f850a6eb1fa08e6c722fda2fe438f484dbde78df218bb274c7
Initial #check passed
DELETE FROM Plot WHERE PlotId = '3';
prev blc #: 44f0043dba16d5f850a6eb1fa08e6c722fda2fe438f484dbde78df218bb274c7
curr table#: 0xffd1bc4723d4d57f740acf5bc1e4348b8f93153a1f3d03d7ecad24beeae69748
transformed blc: deletePlotRecord('3',True)
revert func: rollbackDeletePlotRecord('3')
curr blc#: ffd1bc4723d4d57f740acf5bc1e4348b8f93153a1f3d03d7ecad24beeae69748
hash match status: pass

*************

Reverted
curr table#: 44f0043dba16d5f850a6eb1fa08e6c722fda2fe438f484dbde78df218bb274c7
curr blc#: 44f0043dba16d5f850a6eb1fa08e6c722fda2fe438f484dbde78df218bb274c7

```

## Test 6

#### Input

```
INSERT INTO Plot (PlotId,  PlotInfo) VALUE('1','kl_clt_01');
INSERT INTO Plot (PlotId, PlotInfo) VALUE('2','kl_tvc_02');
INSERT INTO Plot (PlotId, PlotInfo) VALUE('3','dl_del_03');
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('101','81','1');
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('201','82','2');  
UPDATE Khatauni SET Kid = '401' WHERE KId = 101;
UPDATE Khatauni SET Aadhar = '481' WHERE KId = 401;
UPDATE Khatauni SET Pid = '1' WHERE KId = 201;
UPDATE Plot SET Plotid = '503' WHERE PlotId = 3;
UPDATE Plot SET Plotid = '501' WHERE PlotId = 2;
```

#### Output
```
Initial #check passed
INSERT INTO Plot (PlotId,  PlotInfo) VALUE('1','kl_clt_01');
prev blc #: 0000000000000000000000000000000000000000000000000000000000000000
curr table#: 0xede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
transformed blc: createPlotEntry('1','kl_clt_01',True)
revert func: deletePlotRecord('1',False)
curr blc#: ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
hash match status: pass

*************

Initial #check passed
INSERT INTO Plot (PlotId, PlotInfo) VALUE('2','kl_tvc_02');
prev blc #: ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
curr table#: 0x5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
transformed blc: createPlotEntry('2','kl_tvc_02',True)
revert func: deletePlotRecord('2',False)
curr blc#: 5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
hash match status: pass

*************

Initial #check passed
INSERT INTO Plot (PlotId, PlotInfo) VALUE('3','dl_del_03');
prev blc #: 5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
curr table#: 0x046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
transformed blc: createPlotEntry('3','dl_del_03',True)
revert func: deletePlotRecord('3',False)
curr blc#: 046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
hash match status: pass

*************

Initial #check passed
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('101','81','1');
prev blc #: 046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
curr table#: 0xbce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
transformed blc: createKhatauniEntry('101','81','1',True)
revert func: deleteKhatauniRecord('101',False)
curr blc#: bce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
hash match status: pass

*************

Initial #check passed
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('201','82','2');
prev blc #: bce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
curr table#: 0x9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
transformed blc: createKhatauniEntry('201','82','2',True)
revert func: deleteKhatauniRecord('201',False)
curr blc#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
hash match status: pass

*************

Initial #check passed
UPDATE Khatauni SET Kid = '401' WHERE KId = 101;
prev blc #: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr table#: 0x3f24cb8f13fb2800d49b2a9b33041ec5320be3a2770c3c58ac9b7fe67a8c1ead
transformed blc: updateKhatauniKid('101', '401',True)
revert func: updateKhatauniKid('401','101', False)
prev val exp: SELECT Kid FROM Khatauni WHERE Kid = '101' LIMIT 1;
fetched prev val: 101
curr blc#: 3f24cb8f13fb2800d49b2a9b33041ec5320be3a2770c3c58ac9b7fe67a8c1ead
hash match status: pass

*************

Initial #check passed
UPDATE Khatauni SET Aadhar = '481' WHERE KId = 401;
prev blc #: 3f24cb8f13fb2800d49b2a9b33041ec5320be3a2770c3c58ac9b7fe67a8c1ead
curr table#: 0x9e0a9e4166571dd1254d9eab9fb1488f06af78971d106221b9af09f94c24576b
transformed blc: updateKhatauniAadhar('401', '481',True)
revert func: updateKhatauniAadhar('401','81', False)
prev val exp: SELECT Aadhar FROM Khatauni WHERE Kid = '401' LIMIT 1;
fetched prev val: 81
curr blc#: 9e0a9e4166571dd1254d9eab9fb1488f06af78971d106221b9af09f94c24576b
hash match status: pass

*************

Initial #check passed
UPDATE Khatauni SET Pid = '1' WHERE KId = 201;
prev blc #: 9e0a9e4166571dd1254d9eab9fb1488f06af78971d106221b9af09f94c24576b
curr table#: 0x92fee76f6f5e97ba729088fcc54d2cea42ec900c4af44228e5d0f850dab362a7
transformed blc: updateKhatauniPid('201', '1',True)
revert func: updateKhatauniPid('201','2', False)
prev val exp: SELECT Pid FROM Khatauni WHERE Kid = '201' LIMIT 1;
fetched prev val: 2
curr blc#: 92fee76f6f5e97ba729088fcc54d2cea42ec900c4af44228e5d0f850dab362a7
hash match status: pass

*************

Initial #check passed
UPDATE Plot SET PlotInfo = 'changed info' WHERE PlotId = 3;
prev blc #: 92fee76f6f5e97ba729088fcc54d2cea42ec900c4af44228e5d0f850dab362a7
curr table#: 0xb526ca90b56db5fbe9b7d6d216ea312047dd5bf014ca9d03b66159f17e42c69c
transformed blc: updatePlotPlotinfo('3', 'changed info',True)
revert func: updatePlotPlotinfo('3','dl_del_03', False)
prev val exp: SELECT PlotInfo FROM Plot WHERE Plotid = '3' LIMIT 1;
fetched prev val: dl_del_03
curr blc#: b526ca90b56db5fbe9b7d6d216ea312047dd5bf014ca9d03b66159f17e42c69c
hash match status: pass

*************

Initial #check passed
UPDATE Plot SET Plotid = '503' WHERE PlotId = 3;
prev blc #: b526ca90b56db5fbe9b7d6d216ea312047dd5bf014ca9d03b66159f17e42c69c
curr table#: 0x7f80a68712f1cd38b4745992709ddda3df534a9bff3b99e14170e74bbe146ff1
transformed blc: updatePlotPlotid('3', '503',True)
revert func: updatePlotPlotid('503','3', False)
prev val exp: SELECT Plotid FROM Plot WHERE Plotid = '3' LIMIT 1;
fetched prev val: 3
curr blc#: 7f80a68712f1cd38b4745992709ddda3df534a9bff3b99e14170e74bbe146ff1
hash match status: pass

*************

Initial #check passed
UPDATE Plot SET Plotid = '501' WHERE PlotId = 2;
prev blc #: 7f80a68712f1cd38b4745992709ddda3df534a9bff3b99e14170e74bbe146ff1
curr table#: 0x7b912afad7aa074b8cc95645a4fbb1048898307807f794a5ae999da58dfd0e1d
transformed blc: updatePlotPlotid('2', '501',True)
revert func: updatePlotPlotid('501','2', False)
prev val exp: SELECT Plotid FROM Plot WHERE Plotid = '2' LIMIT 1;
fetched prev val: 2
curr blc#: 7b912afad7aa074b8cc95645a4fbb1048898307807f794a5ae999da58dfd0e1d
hash match status: pass

*************


```

## Test 7

first ran insert records without revert
updated and reverted updates

#### Input

```
UPDATE Khatauni SET Kid = '401' WHERE KId = '101';
UPDATE Khatauni SET Aadhar = '481' WHERE KId = '201';
UPDATE Khatauni SET Pid = '3' WHERE KId = '101';
UPDATE Plot SET PlotInfo = 'changed info' WHERE PlotId = '3';
UPDATE Plot SET Plotid = '503' WHERE PlotId = '3';
```

#### Output

```
9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
Initial #check passed
UPDATE Khatauni SET Kid = '401' WHERE KId = '101';
prev blc #: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr table#: 0x3f24cb8f13fb2800d49b2a9b33041ec5320be3a2770c3c58ac9b7fe67a8c1ead
transformed blc: updateKhatauniKid('101', '401',True)
revert func: updateKhatauniKid('401','101', False)
prev val exp: SELECT Kid FROM Khatauni WHERE Kid = '101' LIMIT 1;
fetched prev val: 101
curr blc#: 3f24cb8f13fb2800d49b2a9b33041ec5320be3a2770c3c58ac9b7fe67a8c1ead
hash match status: fail

*************

Reverted
curr table#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr blc#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69

---------

9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
Initial #check passed
UPDATE Khatauni SET Aadhar = '481' WHERE KId = '201';
prev blc #: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr table#: 0x3b77c0e2f5ca5e34565693f7c9941937eb3d296636c6daa294892b40753bde6a
transformed blc: updateKhatauniAadhar('201', '481',True)
revert func: updateKhatauniAadhar('201','82', False)
prev val exp: SELECT Aadhar FROM Khatauni WHERE Kid = '201' LIMIT 1;
fetched prev val: 82
curr blc#: 3b77c0e2f5ca5e34565693f7c9941937eb3d296636c6daa294892b40753bde6a
hash match status: fail

*************

Reverted
curr table#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr blc#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69

---------

9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
Initial #check passed
UPDATE Khatauni SET Pid = '3' WHERE KId = '101';
prev blc #: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr table#: 0x0a63e20a5bee0f2b91d02c637cec1fa063da81fda0367d56b33e0f47972af94a
transformed blc: updateKhatauniPid('101', '3',True)
revert func: updateKhatauniPid('101','1', False)
prev val exp: SELECT Pid FROM Khatauni WHERE Kid = '101' LIMIT 1;
fetched prev val: 1
curr blc#: 0a63e20a5bee0f2b91d02c637cec1fa063da81fda0367d56b33e0f47972af94a
hash match status: fail

*************

Reverted
curr table#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr blc#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69

---------

9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
Initial #check passed
UPDATE Plot SET PlotInfo = 'changed info' WHERE PlotId = '3';
prev blc #: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr table#: 0x26c948408bd19787c3c07dce1f5af1e1bc6520f3d433b7192c2c54ea3df9eb1a
transformed blc: updatePlotPlotinfo('3', 'changed info',True)
revert func: updatePlotPlotinfo('3','dl_del_03', False)
prev val exp: SELECT PlotInfo FROM Plot WHERE Plotid = '3' LIMIT 1;
fetched prev val: dl_del_03
curr blc#: 26c948408bd19787c3c07dce1f5af1e1bc6520f3d433b7192c2c54ea3df9eb1a
hash match status: fail

*************

Reverted
curr table#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr blc#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69

---------

9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
Initial #check passed
UPDATE Plot SET Plotid = '503' WHERE PlotId = '3';
prev blc #: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr table#: 0x5fe52ec64debdf5831f090505a1936c5aa31a665d4eb3a8e43ef7bdf380c68e0
transformed blc: updatePlotPlotid('3', '503',True)
revert func: updatePlotPlotid('503','3', False)
prev val exp: SELECT Plotid FROM Plot WHERE Plotid = '3' LIMIT 1;
fetched prev val: 3
curr blc#: 5fe52ec64debdf5831f090505a1936c5aa31a665d4eb3a8e43ef7bdf380c68e0
hash match status: fail

*************

Reverted
curr table#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr blc#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69

---------


```

## Test 8

Insert update delete

#### Input

```
INSERT INTO Plot (PlotId, PlotInfo) VALUES ('1','kl_clt_01');
INSERT INTO Plot (PlotId, PlotInfo) VALUES ('2','kl_tvc_02');
INSERT INTO Plot (PlotId, PlotInfo) VALUES ('3','dl_del_03');
INSERT INTO Khatauni (KId, Aadhar, PId) VALUES ('101','81','1');
INSERT INTO Khatauni (KId, Aadhar, PId) VALUES ('201','82','2');
UPDATE Khatauni SET Kid = '401' WHERE Kid = '101';
UPDATE Khatauni SET Aadhar = '481' WHERE Kid = '401';
UPDATE Khatauni SET Pid = '1' WHERE Kid = '201';
UPDATE Plot SET PlotInfo = 'changed info' WHERE Plotid = '3';
UPDATE Plot SET Plotid = '503' WHERE Plotid = '3';
UPDATE Plot SET Plotid = '502' WHERE Plotid = '2';
DELETE FROM Plot WHERE PlotId = '502';
DELETE FROM Plot WHERE PlotId = '503';
DELETE FROM Khatauni WHERE KId = '401';
DELETE FROM Khatauni WHERE KId = '201';
DELETE FROM Plot WHERE PlotId = '1';
```


#### Output

```
Initial #check passed
INSERT INTO Plot (PlotId, PlotInfo) VALUES ('1','kl_clt_01');
prev blc #: 0000000000000000000000000000000000000000000000000000000000000000
curr table#: 0xede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
transformed blc: createPlotEntry('1','kl_clt_01',True)
revert func: deletePlotRecord('1',False)
curr blc#: ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
hash match status: pass

*************

ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
Initial #check passed
INSERT INTO Plot (PlotId, PlotInfo) VALUES ('2','kl_tvc_02');
prev blc #: ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
curr table#: 0x5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
transformed blc: createPlotEntry('2','kl_tvc_02',True)
revert func: deletePlotRecord('2',False)
curr blc#: 5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
hash match status: pass

*************

5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
Initial #check passed
INSERT INTO Plot (PlotId, PlotInfo) VALUES ('3','dl_del_03');
prev blc #: 5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
curr table#: 0x046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
transformed blc: createPlotEntry('3','dl_del_03',True)
revert func: deletePlotRecord('3',False)
curr blc#: 046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
hash match status: pass

*************

046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
Initial #check passed
INSERT INTO Khatauni (KId, Aadhar, PId) VALUES ('101','81','1');
prev blc #: 046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
curr table#: 0xbce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
transformed blc: createKhatauniEntry('101','81','1',True)
revert func: deleteKhatauniRecord('101',False)
curr blc#: bce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
hash match status: pass

*************

bce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
Initial #check passed
INSERT INTO Khatauni (KId, Aadhar, PId) VALUES ('201','82','2');
prev blc #: bce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
curr table#: 0x9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
transformed blc: createKhatauniEntry('201','82','2',True)
revert func: deleteKhatauniRecord('201',False)
curr blc#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
hash match status: pass

*************

9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
Initial #check passed
UPDATE Khatauni SET Kid = '401' WHERE Kid = '101';
prev blc #: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr table#: 0x3f24cb8f13fb2800d49b2a9b33041ec5320be3a2770c3c58ac9b7fe67a8c1ead
transformed blc: updateKhatauniKid('101', '401',True)
revert func: updateKhatauniKid('401','101', False)
prev val exp: SELECT Kid FROM Khatauni WHERE Kid = '101' LIMIT 1;
fetched prev val: 101
curr blc#: 3f24cb8f13fb2800d49b2a9b33041ec5320be3a2770c3c58ac9b7fe67a8c1ead
hash match status: pass

*************

3f24cb8f13fb2800d49b2a9b33041ec5320be3a2770c3c58ac9b7fe67a8c1ead
Initial #check passed
UPDATE Khatauni SET Aadhar = '481' WHERE Kid = '401';
prev blc #: 3f24cb8f13fb2800d49b2a9b33041ec5320be3a2770c3c58ac9b7fe67a8c1ead
curr table#: 0x9e0a9e4166571dd1254d9eab9fb1488f06af78971d106221b9af09f94c24576b
transformed blc: updateKhatauniAadhar('401', '481',True)
revert func: updateKhatauniAadhar('401','81', False)
prev val exp: SELECT Aadhar FROM Khatauni WHERE Kid = '401' LIMIT 1;
fetched prev val: 81
curr blc#: 9e0a9e4166571dd1254d9eab9fb1488f06af78971d106221b9af09f94c24576b
hash match status: pass

*************

9e0a9e4166571dd1254d9eab9fb1488f06af78971d106221b9af09f94c24576b
Initial #check passed
UPDATE Khatauni SET Pid = '1' WHERE Kid = '201';
prev blc #: 9e0a9e4166571dd1254d9eab9fb1488f06af78971d106221b9af09f94c24576b
curr table#: 0x92fee76f6f5e97ba729088fcc54d2cea42ec900c4af44228e5d0f850dab362a7
transformed blc: updateKhatauniPid('201', '1',True)
revert func: updateKhatauniPid('201','2', False)
prev val exp: SELECT Pid FROM Khatauni WHERE Kid = '201' LIMIT 1;
fetched prev val: 2
curr blc#: 92fee76f6f5e97ba729088fcc54d2cea42ec900c4af44228e5d0f850dab362a7
hash match status: pass

*************

92fee76f6f5e97ba729088fcc54d2cea42ec900c4af44228e5d0f850dab362a7
Initial #check passed
UPDATE Plot SET PlotInfo = 'changed info' WHERE Plotid = '3';
prev blc #: 92fee76f6f5e97ba729088fcc54d2cea42ec900c4af44228e5d0f850dab362a7
curr table#: 0xb526ca90b56db5fbe9b7d6d216ea312047dd5bf014ca9d03b66159f17e42c69c
transformed blc: updatePlotPlotinfo('3', 'changed info',True)
revert func: updatePlotPlotinfo('3','dl_del_03', False)
prev val exp: SELECT PlotInfo FROM Plot WHERE Plotid = '3' LIMIT 1;
fetched prev val: dl_del_03
curr blc#: b526ca90b56db5fbe9b7d6d216ea312047dd5bf014ca9d03b66159f17e42c69c
hash match status: pass

*************

b526ca90b56db5fbe9b7d6d216ea312047dd5bf014ca9d03b66159f17e42c69c
Initial #check passed
UPDATE Plot SET Plotid = '503' WHERE Plotid = '3';
prev blc #: b526ca90b56db5fbe9b7d6d216ea312047dd5bf014ca9d03b66159f17e42c69c
curr table#: 0x7f80a68712f1cd38b4745992709ddda3df534a9bff3b99e14170e74bbe146ff1
transformed blc: updatePlotPlotid('3', '503',True)
revert func: updatePlotPlotid('503','3', False)
prev val exp: SELECT Plotid FROM Plot WHERE Plotid = '3' LIMIT 1;
fetched prev val: 3
curr blc#: 7f80a68712f1cd38b4745992709ddda3df534a9bff3b99e14170e74bbe146ff1
hash match status: pass

*************

7f80a68712f1cd38b4745992709ddda3df534a9bff3b99e14170e74bbe146ff1
Initial #check passed
UPDATE Plot SET Plotid = '502' WHERE Plotid = '2';
prev blc #: 7f80a68712f1cd38b4745992709ddda3df534a9bff3b99e14170e74bbe146ff1
curr table#: 0xf1e116f13edb74a71030108ceb48eeafe43b81d4205edbcce74067d836a6a3dd
transformed blc: updatePlotPlotid('2', '502',True)
revert func: updatePlotPlotid('502','2', False)
prev val exp: SELECT Plotid FROM Plot WHERE Plotid = '2' LIMIT 1;
fetched prev val: 2
curr blc#: f1e116f13edb74a71030108ceb48eeafe43b81d4205edbcce74067d836a6a3dd
hash match status: pass

*************

f1e116f13edb74a71030108ceb48eeafe43b81d4205edbcce74067d836a6a3dd
Initial #check passed
DELETE FROM Plot WHERE PlotId = '502';
prev blc #: f1e116f13edb74a71030108ceb48eeafe43b81d4205edbcce74067d836a6a3dd
curr table#: 0x79407596be0cfe79757bd718aaa1bec12858bf7f473d3c1b2f40cf6cd0e4ff75
transformed blc: deletePlotRecord('502',True)
revert func: rollbackDeletePlotRecord('502')
curr blc#: 79407596be0cfe79757bd718aaa1bec12858bf7f473d3c1b2f40cf6cd0e4ff75
hash match status: pass

*************

79407596be0cfe79757bd718aaa1bec12858bf7f473d3c1b2f40cf6cd0e4ff75
Initial #check passed
DELETE FROM Plot WHERE PlotId = '503';
prev blc #: 79407596be0cfe79757bd718aaa1bec12858bf7f473d3c1b2f40cf6cd0e4ff75
curr table#: 0x265b0ca18764cebec8f2ea0f6cf0b381ea9d0afffc9e8e8cfe442ce1434d9c62
transformed blc: deletePlotRecord('503',True)
revert func: rollbackDeletePlotRecord('503')
curr blc#: 265b0ca18764cebec8f2ea0f6cf0b381ea9d0afffc9e8e8cfe442ce1434d9c62
hash match status: pass

*************

265b0ca18764cebec8f2ea0f6cf0b381ea9d0afffc9e8e8cfe442ce1434d9c62
Initial #check passed
DELETE FROM Khatauni WHERE KId = '401';
prev blc #: 265b0ca18764cebec8f2ea0f6cf0b381ea9d0afffc9e8e8cfe442ce1434d9c62
curr table#: 0x1581e8bb6f8622e23a70dfa0194e3024df6f39c2e15152eb1929cd97c1bfaab2
transformed blc: deleteKhatauniRecord('401',True)
revert func: rollbackDeleteKhatauniRecord('401')
curr blc#: 1581e8bb6f8622e23a70dfa0194e3024df6f39c2e15152eb1929cd97c1bfaab2
hash match status: pass

*************

1581e8bb6f8622e23a70dfa0194e3024df6f39c2e15152eb1929cd97c1bfaab2
Initial #check passed
DELETE FROM Khatauni WHERE KId = '201';
prev blc #: 1581e8bb6f8622e23a70dfa0194e3024df6f39c2e15152eb1929cd97c1bfaab2
curr table#: 0x0fdc0ff8be34f93d0059f977d2310697509e260537bbff72496d46ba4363f198
transformed blc: deleteKhatauniRecord('201',True)
revert func: rollbackDeleteKhatauniRecord('201')
curr blc#: 0fdc0ff8be34f93d0059f977d2310697509e260537bbff72496d46ba4363f198
hash match status: pass

*************

0fdc0ff8be34f93d0059f977d2310697509e260537bbff72496d46ba4363f198
Initial #check passed
DELETE FROM Plot WHERE PlotId = '1';
prev blc #: 0fdc0ff8be34f93d0059f977d2310697509e260537bbff72496d46ba4363f198
curr table#: 0xe982f1c522c8b2c32752b99bb4137e500491757f63aac62dea7b57a2a90133fd
transformed blc: deletePlotRecord('1',True)
revert func: rollbackDeletePlotRecord('1')
curr blc#: e982f1c522c8b2c32752b99bb4137e500491757f63aac62dea7b57a2a90133fd
hash match status: pass


```

