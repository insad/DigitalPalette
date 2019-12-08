for i in 0 1 2 3 4 5 6 7 8; do
  convert -resize "535x426" "${i}.png" "${i}.png"
done
