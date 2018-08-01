img = imread('mapSocietyMod.png');
% size(img)
img = rgb2gray(img);
img = img > 250;
close all

imshow(img)
size(img) 
mskel = bwmorph(img, 'skel', Inf);
figure, imshow(mskel)