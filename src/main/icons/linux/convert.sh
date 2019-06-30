convert "1024.png" "1024.png"

for i in 512 256 128; do
  convert -resize "${i}x${i}" "1024.png" "${i}.png"
done

for i in 64 48 32 24 16; do
  convert -resize "${i}x${i}" "1024.png" "../base/${i}.png"
done

convert "256.png" "../Icon.ico"
