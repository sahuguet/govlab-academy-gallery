rm gen/*
python generate.py
(cd gen; ln -s ../assets .; ln -s ../scss .)
echo "done"
