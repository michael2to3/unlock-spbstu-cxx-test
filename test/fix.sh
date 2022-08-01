#!/usr/bin/env fish

for i in test*;
  mv $i (echo $i | string replace -a '-' '').py
end

sd 'from labtesting' 'from test.labtesting' ./*py
