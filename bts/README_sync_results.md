## Test 1
#### Input

###### sync_sql_blc_test.txt

```
createPlotEntry('1','kl_clt_01')
createPlotEntry('2','kl_tvc_02')
createPlotEntry('3','dl_del_03')
createKhatauniEntry('101','81','1')
createKhatauniEntry('201','82','2') 
```


#### Output

```
Initial #check passed
createPlotEntry('1','kl_clt_01')
prev blc #: 0000000000000000000000000000000000000000000000000000000000000000
equivalent sql: INSERT INTO Plot (PlotId, PlotInfo) VALUES ('1','kl_clt_01');
transformed blc: createPlotEntry('1','kl_clt_01',True)
revert func: deletePlotRecord('1',False)
curr table#: 0000000000000000000000000000000000000000000000000000000000000000
curr blc#: ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
hash match status: pass

*************

Initial #check passed
createPlotEntry('2','kl_tvc_02')
prev blc #: ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
equivalent sql: INSERT INTO Plot (PlotId, PlotInfo) VALUES ('2','kl_tvc_02');
transformed blc: createPlotEntry('2','kl_tvc_02',True)
revert func: deletePlotRecord('2',False)
curr table#: 0xede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
curr blc#: 5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
hash match status: pass

*************

Initial #check passed
createPlotEntry('3','dl_del_03')
prev blc #: 5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
equivalent sql: INSERT INTO Plot (PlotId, PlotInfo) VALUES ('3','dl_del_03');
transformed blc: createPlotEntry('3','dl_del_03',True)
revert func: deletePlotRecord('3',False)
curr table#: 0x5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
curr blc#: 046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
hash match status: pass

*************

Initial #check passed
createKhatauniEntry('101','81','1')
prev blc #: 046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
equivalent sql: INSERT INTO Khatauni (KId, Aadhar, PId) VALUES ('101','81','1');
transformed blc: createKhatauniEntry('101','81','1',True)
revert func: deleteKhatauniRecord('101',False)
curr table#: 0x046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
curr blc#: bce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
hash match status: pass

*************

Initial #check passed
createKhatauniEntry('201','82','2')
prev blc #: bce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
equivalent sql: INSERT INTO Khatauni (KId, Aadhar, PId) VALUES ('201','82','2');
transformed blc: createKhatauniEntry('201','82','2',True)
revert func: deleteKhatauniRecord('201',False)
curr table#: 0xbce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
curr blc#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
hash match status: pass

*************


```

## Test 2
#### Input

###### sync_sql_blc_test.txt

```
createPlotEntry('1','kl_clt_01')
createPlotEntry('2','kl_tvc_02')
createPlotEntry('3','dl_del_03')
createKhatauniEntry('101','81','1')
createKhatauniEntry('201','82','2') 
updateKhatauniKid('101', '401')
updateKhatauniAadhar('401', '481')
updateKhatauniPid('201', '1')
updatePlotPlotinfo('3', 'changed info')
updatePlotPlotid('3', '503')
updatePlotPlotid('2', '501')
```


#### Output

```
Initial #check passed
createPlotEntry('1','kl_clt_01')
prev blc #: 0000000000000000000000000000000000000000000000000000000000000000
equivalent sql: INSERT INTO Plot (PlotId, PlotInfo) VALUES ('1','kl_clt_01');
transformed blc: createPlotEntry('1','kl_clt_01',True)
revert func: deletePlotRecord('1',False)
curr table#: 0000000000000000000000000000000000000000000000000000000000000000
curr blc#: ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
hash match status: pass

*************

Initial #check passed
createPlotEntry('2','kl_tvc_02')
prev blc #: ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
equivalent sql: INSERT INTO Plot (PlotId, PlotInfo) VALUES ('2','kl_tvc_02');
transformed blc: createPlotEntry('2','kl_tvc_02',True)
revert func: deletePlotRecord('2',False)
curr table#: 0xede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
curr blc#: 5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
hash match status: pass

*************

Initial #check passed
createPlotEntry('3','dl_del_03')
prev blc #: 5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
equivalent sql: INSERT INTO Plot (PlotId, PlotInfo) VALUES ('3','dl_del_03');
transformed blc: createPlotEntry('3','dl_del_03',True)
revert func: deletePlotRecord('3',False)
curr table#: 0x5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
curr blc#: 046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
hash match status: pass

*************

Initial #check passed
createKhatauniEntry('101','81','1')
prev blc #: 046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
equivalent sql: INSERT INTO Khatauni (KId, Aadhar, PId) VALUES ('101','81','1');
transformed blc: createKhatauniEntry('101','81','1',True)
revert func: deleteKhatauniRecord('101',False)
curr table#: 0x046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
curr blc#: bce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
hash match status: pass

*************

Initial #check passed
createKhatauniEntry('201','82','2')
prev blc #: bce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
equivalent sql: INSERT INTO Khatauni (KId, Aadhar, PId) VALUES ('201','82','2');
transformed blc: createKhatauniEntry('201','82','2',True)
revert func: deleteKhatauniRecord('201',False)
curr table#: 0xbce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
curr blc#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
hash match status: pass

*************

Initial #check passed
updateKhatauniKid('101', '401')
prev blc #: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
equivalent sql: UPDATE Khatauni SET Kid = '401' WHERE Kid = '101';
transformed blc: updateKhatauniKid('101', '401',True)
revert func: updateKhatauniKid('401','101', False)
prev val exp: SELECT Kid FROM Khatauni WHERE Kid = '101' LIMIT 1;
fetched prev val: 101
curr table#: 0x9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr blc#: 3f24cb8f13fb2800d49b2a9b33041ec5320be3a2770c3c58ac9b7fe67a8c1ead
hash match status: pass

*************

Initial #check passed
updateKhatauniAadhar('401', '481')
prev blc #: 3f24cb8f13fb2800d49b2a9b33041ec5320be3a2770c3c58ac9b7fe67a8c1ead
equivalent sql: UPDATE Khatauni SET Aadhar = '481' WHERE Kid = '401';
transformed blc: updateKhatauniAadhar('401', '481',True)
revert func: updateKhatauniAadhar('401','81', False)
prev val exp: SELECT Aadhar FROM Khatauni WHERE Kid = '401' LIMIT 1;
fetched prev val: 81
curr table#: 0x3f24cb8f13fb2800d49b2a9b33041ec5320be3a2770c3c58ac9b7fe67a8c1ead
curr blc#: 9e0a9e4166571dd1254d9eab9fb1488f06af78971d106221b9af09f94c24576b
hash match status: pass

*************

Initial #check passed
updateKhatauniPid('201', '1')
prev blc #: 9e0a9e4166571dd1254d9eab9fb1488f06af78971d106221b9af09f94c24576b
equivalent sql: UPDATE Khatauni SET Pid = '1' WHERE Kid = '201';
transformed blc: updateKhatauniPid('201', '1',True)
revert func: updateKhatauniPid('201','2', False)
prev val exp: SELECT Pid FROM Khatauni WHERE Kid = '201' LIMIT 1;
fetched prev val: 2
curr table#: 0x9e0a9e4166571dd1254d9eab9fb1488f06af78971d106221b9af09f94c24576b
curr blc#: 92fee76f6f5e97ba729088fcc54d2cea42ec900c4af44228e5d0f850dab362a7
hash match status: pass

*************

Initial #check passed
updatePlotPlotinfo('3', 'changed info')
prev blc #: 92fee76f6f5e97ba729088fcc54d2cea42ec900c4af44228e5d0f850dab362a7
equivalent sql: UPDATE Plot SET Plotinfo = 'changed info' WHERE Plotid = '3';
transformed blc: updatePlotPlotinfo('3', 'changed info',True)
revert func: updatePlotPlotinfo('3','dl_del_03', False)
prev val exp: SELECT Plotinfo FROM Plot WHERE Plotid = '3' LIMIT 1;
fetched prev val: dl_del_03
curr table#: 0x92fee76f6f5e97ba729088fcc54d2cea42ec900c4af44228e5d0f850dab362a7
curr blc#: b526ca90b56db5fbe9b7d6d216ea312047dd5bf014ca9d03b66159f17e42c69c
hash match status: pass

*************

Initial #check passed
updatePlotPlotid('3', '503')
prev blc #: b526ca90b56db5fbe9b7d6d216ea312047dd5bf014ca9d03b66159f17e42c69c
equivalent sql: UPDATE Plot SET Plotid = '503' WHERE Plotid = '3';
transformed blc: updatePlotPlotid('3', '503',True)
revert func: updatePlotPlotid('503','3', False)
prev val exp: SELECT Plotid FROM Plot WHERE Plotid = '3' LIMIT 1;
fetched prev val: 3
curr table#: 0xb526ca90b56db5fbe9b7d6d216ea312047dd5bf014ca9d03b66159f17e42c69c
curr blc#: 7f80a68712f1cd38b4745992709ddda3df534a9bff3b99e14170e74bbe146ff1
hash match status: pass

*************

Initial #check passed
updatePlotPlotid('2', '501')
prev blc #: 7f80a68712f1cd38b4745992709ddda3df534a9bff3b99e14170e74bbe146ff1
equivalent sql: UPDATE Plot SET Plotid = '501' WHERE Plotid = '2';
transformed blc: updatePlotPlotid('2', '501',True)
revert func: updatePlotPlotid('501','2', False)
prev val exp: SELECT Plotid FROM Plot WHERE Plotid = '2' LIMIT 1;
fetched prev val: 2
curr table#: 0x7f80a68712f1cd38b4745992709ddda3df534a9bff3b99e14170e74bbe146ff1
curr blc#: 7b912afad7aa074b8cc95645a4fbb1048898307807f794a5ae999da58dfd0e1d
hash match status: pass

*************

```

## Test 3
#### Input

###### sync_sql_blc_test.txt

```
createPlotEntry('1','kl_clt_01')
createPlotEntry('2','kl_tvc_02')
createPlotEntry('3','dl_del_03')
createKhatauniEntry('101','81','1')
createKhatauniEntry('201','82','2')
updateKhatauniKid('101', '401')
updateKhatauniAadhar('401', '481')
updateKhatauniPid('201', '1')
updatePlotPlotinfo('3', 'changed info')
updatePlotPlotid('3', '503')
updatePlotPlotid('2', '502')
deletePlotRecord('502')
deletePlotRecord('503')
deleteKhatauniRecord('401')
deleteKhatauniRecord('201')
deletePlotRecord('1')
```


#### Output

```
Initial #check passed
createPlotEntry('1','kl_clt_01')
prev blc #: 0000000000000000000000000000000000000000000000000000000000000000
equivalent sql: INSERT INTO Plot (PlotId, PlotInfo) VALUES ('1','kl_clt_01');
transformed blc: createPlotEntry('1','kl_clt_01',True)
revert func: deletePlotRecord('1',False)
curr table#: 0000000000000000000000000000000000000000000000000000000000000000
curr blc#: ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
hash match status: pass

*************

Initial #check passed
createPlotEntry('2','kl_tvc_02')
prev blc #: ede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
equivalent sql: INSERT INTO Plot (PlotId, PlotInfo) VALUES ('2','kl_tvc_02');
transformed blc: createPlotEntry('2','kl_tvc_02',True)
revert func: deletePlotRecord('2',False)
curr table#: 0xede1e7893a23c7cf0542f1318db0623a09d6fed6f72e5e8ea7eadfa66900f4ba
curr blc#: 5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
hash match status: pass

*************

Initial #check passed
createPlotEntry('3','dl_del_03')
prev blc #: 5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
equivalent sql: INSERT INTO Plot (PlotId, PlotInfo) VALUES ('3','dl_del_03');
transformed blc: createPlotEntry('3','dl_del_03',True)
revert func: deletePlotRecord('3',False)
curr table#: 0x5da410854b505bb021affd0d46cc96b35b46528c750007b16c5ccfa24cff011f
curr blc#: 046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
hash match status: pass

*************

Initial #check passed
createKhatauniEntry('101','81','1')
prev blc #: 046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
equivalent sql: INSERT INTO Khatauni (KId, Aadhar, PId) VALUES ('101','81','1');
transformed blc: createKhatauniEntry('101','81','1',True)
revert func: deleteKhatauniRecord('101',False)
curr table#: 0x046f9982895c0cc9d40454be1c71b30e0e7eb442b457bad18a460adfca36955d
curr blc#: bce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
hash match status: pass

*************

Initial #check passed
createKhatauniEntry('201','82','2')
prev blc #: bce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
equivalent sql: INSERT INTO Khatauni (KId, Aadhar, PId) VALUES ('201','82','2');
transformed blc: createKhatauniEntry('201','82','2',True)
revert func: deleteKhatauniRecord('201',False)
curr table#: 0xbce60cdfb645313d194be63ed6b892979175ce28de83885fed6b26c6ff8560c6
curr blc#: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
hash match status: pass

*************

Initial #check passed
updateKhatauniKid('101', '401')
prev blc #: 9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
equivalent sql: UPDATE Khatauni SET Kid = '401' WHERE Kid = '101';
transformed blc: updateKhatauniKid('101', '401',True)
revert func: updateKhatauniKid('401','101', False)
prev val exp: SELECT Kid FROM Khatauni WHERE Kid = '101' LIMIT 1;
fetched prev val: 101
curr table#: 0x9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69
curr blc#: 3f24cb8f13fb2800d49b2a9b33041ec5320be3a2770c3c58ac9b7fe67a8c1ead
hash match status: pass

*************

Initial #check passed
updateKhatauniAadhar('401', '481')
prev blc #: 3f24cb8f13fb2800d49b2a9b33041ec5320be3a2770c3c58ac9b7fe67a8c1ead
equivalent sql: UPDATE Khatauni SET Aadhar = '481' WHERE Kid = '401';
transformed blc: updateKhatauniAadhar('401', '481',True)
revert func: updateKhatauniAadhar('401','81', False)
prev val exp: SELECT Aadhar FROM Khatauni WHERE Kid = '401' LIMIT 1;
fetched prev val: 81
curr table#: 0x3f24cb8f13fb2800d49b2a9b33041ec5320be3a2770c3c58ac9b7fe67a8c1ead
curr blc#: 9e0a9e4166571dd1254d9eab9fb1488f06af78971d106221b9af09f94c24576b
hash match status: pass

*************

Initial #check passed
updateKhatauniPid('201', '1')
prev blc #: 9e0a9e4166571dd1254d9eab9fb1488f06af78971d106221b9af09f94c24576b
equivalent sql: UPDATE Khatauni SET Pid = '1' WHERE Kid = '201';
transformed blc: updateKhatauniPid('201', '1',True)
revert func: updateKhatauniPid('201','2', False)
prev val exp: SELECT Pid FROM Khatauni WHERE Kid = '201' LIMIT 1;
fetched prev val: 2
curr table#: 0x9e0a9e4166571dd1254d9eab9fb1488f06af78971d106221b9af09f94c24576b
curr blc#: 92fee76f6f5e97ba729088fcc54d2cea42ec900c4af44228e5d0f850dab362a7
hash match status: pass

*************

Initial #check passed
updatePlotPlotinfo('3', 'changed info')
prev blc #: 92fee76f6f5e97ba729088fcc54d2cea42ec900c4af44228e5d0f850dab362a7
equivalent sql: UPDATE Plot SET Plotinfo = 'changed info' WHERE Plotid = '3';
transformed blc: updatePlotPlotinfo('3', 'changed info',True)
revert func: updatePlotPlotinfo('3','dl_del_03', False)
prev val exp: SELECT Plotinfo FROM Plot WHERE Plotid = '3' LIMIT 1;
fetched prev val: dl_del_03
curr table#: 0x92fee76f6f5e97ba729088fcc54d2cea42ec900c4af44228e5d0f850dab362a7
curr blc#: b526ca90b56db5fbe9b7d6d216ea312047dd5bf014ca9d03b66159f17e42c69c
hash match status: pass

*************

Initial #check passed
updatePlotPlotid('3', '503')
prev blc #: b526ca90b56db5fbe9b7d6d216ea312047dd5bf014ca9d03b66159f17e42c69c
equivalent sql: UPDATE Plot SET Plotid = '503' WHERE Plotid = '3';
transformed blc: updatePlotPlotid('3', '503',True)
revert func: updatePlotPlotid('503','3', False)
prev val exp: SELECT Plotid FROM Plot WHERE Plotid = '3' LIMIT 1;
fetched prev val: 3
curr table#: 0xb526ca90b56db5fbe9b7d6d216ea312047dd5bf014ca9d03b66159f17e42c69c
curr blc#: 7f80a68712f1cd38b4745992709ddda3df534a9bff3b99e14170e74bbe146ff1
hash match status: pass

*************

Initial #check passed
updatePlotPlotid('2', '502')
prev blc #: 7f80a68712f1cd38b4745992709ddda3df534a9bff3b99e14170e74bbe146ff1
equivalent sql: UPDATE Plot SET Plotid = '502' WHERE Plotid = '2';
transformed blc: updatePlotPlotid('2', '502',True)
revert func: updatePlotPlotid('502','2', False)
prev val exp: SELECT Plotid FROM Plot WHERE Plotid = '2' LIMIT 1;
fetched prev val: 2
curr table#: 0x7f80a68712f1cd38b4745992709ddda3df534a9bff3b99e14170e74bbe146ff1
curr blc#: f1e116f13edb74a71030108ceb48eeafe43b81d4205edbcce74067d836a6a3dd
hash match status: pass

*************

Initial #check passed
deletePlotRecord('502')
prev blc #: f1e116f13edb74a71030108ceb48eeafe43b81d4205edbcce74067d836a6a3dd
equivalent sql: DELETE FROM Plot WHERE PlotId = '502';
transformed blc: deletePlotRecord('502',True)
revert func: rollbackDeletePlotRecord('502')
curr table#: 0xf1e116f13edb74a71030108ceb48eeafe43b81d4205edbcce74067d836a6a3dd
curr blc#: 79407596be0cfe79757bd718aaa1bec12858bf7f473d3c1b2f40cf6cd0e4ff75
hash match status: pass

*************

Initial #check passed
deletePlotRecord('503')
prev blc #: 79407596be0cfe79757bd718aaa1bec12858bf7f473d3c1b2f40cf6cd0e4ff75
equivalent sql: DELETE FROM Plot WHERE PlotId = '503';
transformed blc: deletePlotRecord('503',True)
revert func: rollbackDeletePlotRecord('503')
curr table#: 0x79407596be0cfe79757bd718aaa1bec12858bf7f473d3c1b2f40cf6cd0e4ff75
curr blc#: 265b0ca18764cebec8f2ea0f6cf0b381ea9d0afffc9e8e8cfe442ce1434d9c62
hash match status: pass

*************

Initial #check passed
deleteKhatauniRecord('401')
prev blc #: 265b0ca18764cebec8f2ea0f6cf0b381ea9d0afffc9e8e8cfe442ce1434d9c62
equivalent sql: DELETE FROM Khatauni WHERE KId = '401';
transformed blc: deleteKhatauniRecord('401',True)
revert func: rollbackDeleteKhatauniRecord('401')
curr table#: 0x265b0ca18764cebec8f2ea0f6cf0b381ea9d0afffc9e8e8cfe442ce1434d9c62
curr blc#: 1581e8bb6f8622e23a70dfa0194e3024df6f39c2e15152eb1929cd97c1bfaab2
hash match status: pass

*************

Initial #check passed
deleteKhatauniRecord('201')
prev blc #: 1581e8bb6f8622e23a70dfa0194e3024df6f39c2e15152eb1929cd97c1bfaab2
equivalent sql: DELETE FROM Khatauni WHERE KId = '201';
transformed blc: deleteKhatauniRecord('201',True)
revert func: rollbackDeleteKhatauniRecord('201')
curr table#: 0x1581e8bb6f8622e23a70dfa0194e3024df6f39c2e15152eb1929cd97c1bfaab2
curr blc#: 0fdc0ff8be34f93d0059f977d2310697509e260537bbff72496d46ba4363f198
hash match status: pass

*************

Initial #check passed
deletePlotRecord('1')
prev blc #: 0fdc0ff8be34f93d0059f977d2310697509e260537bbff72496d46ba4363f198
equivalent sql: DELETE FROM Plot WHERE PlotId = '1';
transformed blc: deletePlotRecord('1',True)
revert func: rollbackDeletePlotRecord('1')
curr table#: 0x0fdc0ff8be34f93d0059f977d2310697509e260537bbff72496d46ba4363f198
curr blc#: e982f1c522c8b2c32752b99bb4137e500491757f63aac62dea7b57a2a90133fd
hash match status: pass

*************

```

---


###### schema_dict.txt

```
{"khatauni": {"table_name": "khatauni", "columns": [], "col": [["KId", "varchar(255)"], ["Aadhar", "varchar(255)"], ["PId", "varchar(255)"]], "for_key_dep_on": ["PId -> plot.PlotId"], "pk": "KId"}, "plot": {"table_name": "plot", "columns": [], "col": [["PlotId", "varchar(255)"], ["PlotInfo", "varchar(255)"]], "for_key_dep_on": [], "pk": "PlotId"}}
```
