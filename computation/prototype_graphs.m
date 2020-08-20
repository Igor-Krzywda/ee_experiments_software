#!/usr/bin/octave
arr = csvread(argv(){1});
c1 = arr(:,1);
c2 = arr(:,2);
plot(c1,c2)
print -djpg raw.jpg
arr = csvread(argv(){2});
c1 = arr(:,1);
c2 = arr(:,2);
plot(c1,c2)
print("clean.jpg")
arr = csvread(argv(){3});
c1 = arr(:,1);
c2 = arr(:,2);
plot(c1,c2)
print("super_clean.jpg")
