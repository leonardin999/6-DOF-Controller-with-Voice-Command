% clear all
clc

A =[280.593	;86.8364;
    314.9	;86.7577;
    349.264	;86.7129;
    383.573	;86.7041;
    417.749	;86.715;
    452.107	;86.6789;
    486.381	;86.6444;
    280.674	;121.387;
    314.964	;121.304;
    349.269	;121.248;
    383.496	;121.174;
    417.665	;121.162;
    451.866	;121.154;
    486.101	;121.189;
    280.781	;155.581;
    315.042	;155.529;
    349.315	;155.461;
    383.458	;155.446;
    417.611	;155.449;
    451.72	;155.421;
    485.887	;155.379;
    280.9	;189.768;
    315.13	;189.728;
    349.314	;189.655;
    383.474	;189.618;
    417.535	;189.583;
    451.614	;189.535;
    485.745	;189.518;
    281.093	;223.921;
    315.166	;223.829;
    349.348	;223.757;
    383.448	;223.706;
    417.536	;223.683;
    451.551	;223.599;
    485.621	;223.562];
 
M_rb = [18.8  -10.5;
        18.8  -9   ;
        18.8  -7.5 ;
        18.8  -6   ;
        18.8  -4.5 ;
        18.8  -3   ;
        18.8  -1.5 ;
        20.3  -10.5;
        20.3  -9   ;
        20.3  -7.5 ;
        20.3  -6   ;
        20.3  -4.5 ;
        20.3  -3   ;
        20.3  -1.5 ;
        21.8  -10.5;
        21.8  -9   ;
        21.8  -7.5 ;
        21.8  -6   ;
        21.8  -4.5 ;
        21.8  -3   ;
        21.8  -1.5 ;
        23.3  -10.5;
        23.3  -9   ;
        23.3  -7.5 ;
        23.3  -6   ;
        23.3  -4.5 ;
        23.3  -3   ;
        23.3  -1.5 ;
        24.8  -10.5;
        24.8  -9   ;
        24.8  -7.5 ;
        24.8  -6   ;
        24.8  -4.5 ;
        24.8  -3   ;
        24.8  -1.5];
k = length(M_rb);
for i = 1:k     
  B(2*i-1,:) = [M_rb(i,:)   1    0 0 0     -A(2*i-1)*M_rb(i,1)  -A(2*i-1)*M_rb(i,2)];
  B(2*i,:)   = [0 0      0   M_rb(i,:) 1   -A(2*i)*M_rb(i,1)  -A(2*i)*M_rb(i,2)];
end  

  M = B\A;
  M = ([M ;1]);
  M = reshape(M,[],3)';
  M_iv = inv(M);
  findP = (inv(M))*[ 280.593 ; 86.8364;1];
  X = findP(1)/findP(3);
  Y = findP(2)/findP(3);
  Point=[X;Y];