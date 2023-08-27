store a = 0;
store voti = [[6,8,7,9,8,6.25,7,],[7,7,7.5,6.5,7,6,7.5,],[9,9,9,8,8.5,7.5,8,],[7,7.5,7.75,8.25,8.5,7,7.5,],[7,7.5,7.75,8,8.75,6.76,7,],];
store i = 0;
store somma_media_totale = 0;
store media_totale = 0;
while(i < 5){
    store curr_subj = getAV(voti i);
    store somma = 0;
    store media = 0;
    store n = 0;
    while(n<7){
        store curr_voto = getAV(curr_subj n);
        store somma = somma + curr_voto;
        store n = n + 1;
    }
    store media = somma / 7;
    print("materia_successiva:");
    print(somma);
    print(media);
    store i = i + 1;
    store somma_media_totale = somma_media_totale + media;
}
store media_totale = somma_media_totale/5;
print("___________________________________________");
print("media_totale:");
print(media_totale);
if(media_totale GOE 6){
    print("alunno_ammesso_al_successivo_anno_scolastico");
}
if(media_totale < 6){
    print("alunno_non_ammesso_al_successivo_anno_scolastico");
}
print("___________________________________________");
