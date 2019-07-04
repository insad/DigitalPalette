for i in 0 1 2 3; do
  convert -resize "416x300" "${i}.png" "${i}.png"
done
