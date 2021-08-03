#!/usr/bin/env bash
#conda activate quantaxis && echo "activate quantaxis"
conda info | grep quantaxis
if [ ! $? -eq 0 ]; then
  echo "Please activate quantaxis first "
#  conda activate quantaxis
  exit 1
fi
if [ ! -f "/tmp/rpstop.xlsx" ]; then
 echo "计算RPS" && python done/rpsIndex.py
else
  echo "已计算RPS"
fi
if [ -f "/tmp/rpstop.xlsx" ]; then
  echo "计算RPS10 ..."  && pytest testing/userFunc/test_rpsIndex.py -k "test_readExcel_block10" -v -s --disable-warnings
#  pytest testing/userFunc/test_rpsIndex.py::TestRPSIndex::test_readExcel4 -s --disable-warnings
  pytest testing/userFunc/test_rpsIndex.py::TestRPSIndex::test_readExcel_peroid -s --disable-warnings
  pytest testing/userFunc/test_rpsIndex.py::TestRPSIndex::test_readExcel_peroid_2 -s --disable-warnings
fi
#conda deactivate
