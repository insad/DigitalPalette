for i in "00" "01" "02" "03" "04" "05" "06" "07" "08" "09" "10"; do
  convert -resize "535x426" "${i}.png" "${i}.png"
done
