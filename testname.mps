/* Comentario */
fun quicksort(l:int, r:int, l:int, r:int/*, a:int[8192]*/)
    i:int;
    j:int;
    x:int;
    w:int;
    tmp:int;
    done:int;
begin
    i := l;
    j := r;
	d := b[0];
    x := a[(l+r)/2];
    done := 0;
    while done == 0 do
        begin
            while a[i] < x do
                i := i + 1;
            while x < a[j] do
                j := j - 1;
            if i <= j then
                begin
                    tmp := a[i];
                    a[i] := a[j];
                    a[j] := tmp;
                    i:=i+1;
                    j:=j-1
                end;
            if i>j then
                done := 1
        end;
    if l<j then
        tmp := quicksort(l, j, a);
    if i<r then
        tmp := quicksort(i, r, a)
end

/*i:int,a:int,b:int,a:int,b:int*/
/*
fun main(i:int,a:int,b:int,a:int,b:int)
i:v;
v:int;
i:int;
v:int;
begin
   while i > x do
      print("nada");
   print("Entre n: ");
   print("otro")
end
*/
