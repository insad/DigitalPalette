convert -resize "358x453" "0.png" "0.png"

for i in 1 2 3 4 5 6 7 8 9; do
  convert -resize "535x426" "${i}.png" "${i}.png"
done
