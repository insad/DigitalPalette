convert "linux/1024.png" "linux/1024.png"

for i in 512 256 128; do
  convert -resize "${i}x${i}" "linux/1024.png" "linux/${i}.png"
done

for i in 64 48 32 24 16; do
  convert -resize "${i}x${i}" "linux/1024.png" "base/${i}.png"
done

convert "linux/256.png" "Icon.ico"
