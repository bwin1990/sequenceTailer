Clear["Global`*"];
file = SystemDialogInput["FileOpen"]
If[file =!= $Canceled, dataIn = StringSplit[Import[file, "String"]]] 
prefix = StringSplit[FileBaseName@file, "syn"][[1]]


Counts[StringLength /@ dataIn](*显示序列长度*)
maxLen = Max[StringLength /@ dataIn] 


out = StringPadRight[StringPadRight[ToUpperCase[dataIn], maxLen, "0"],
   maxLen + 5, "AATAT"]


machineNo = InputString["请输入合成仪编号:"]
name = prefix <> "680k_" <> ToString[maxLen + 5] <> "mer_pickout" <> 
  machineNo <> ".txt"
Export[name, out]