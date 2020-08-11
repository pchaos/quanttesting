#
conda activate quantaxis
[ ! -f "/tmp/rpstop.xlsx" ] && python done/rpsIndex.py
[ -f "/tmp/rpstop.xlsx" ] && pytest testing/userFunc/test_rpsIndex.py -k "test_readExcel_block10" -v -s --disable-warnings
conda deactivate
