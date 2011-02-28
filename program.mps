/* Comentario */
fun quicksort(l:int, r:int, a:int[8192])
    i:int;
    j:int;
    x:int;
    w:int;
    tmp:int;
    done:int;
begin
    i := l;
    j := r;
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
fun main()
   v:int[8192];
   i:int;
   n:int;
begin
   print("Entre n: ");
   read(n);
   i := 0;
   while i<n do
     begin
        read(v[i]);
        i := i+1
     end;
   quicksort(0, n-1, v);
   i := 0;
   while i<n-1 do
     begin
        write(v[i]); print(" ");
        if 0 < v[i] - v[i+1] then
        begin
           print("Quicksort falló "); write(i); print("\n") ; return(0)
        end
        else
           i:=i+1
     end;
   write(v[i]);
   print("éxito\n")
end
