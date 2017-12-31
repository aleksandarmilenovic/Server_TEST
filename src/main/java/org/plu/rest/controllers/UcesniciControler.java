package org.plu.rest.controllers;

import org.plu.dao.UcesniciRepository;
import org.plu.entities.Ucesnici;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/ucesnici")
public class UcesniciControler {

    @Autowired
    private UcesniciRepository ucesniciRepository;

    @GetMapping("/new/{ime}/{prezime}/{indeks}")
    public Ucesnici addNEW(@PathVariable(value = "ime") String ime,@PathVariable(value = "prezime") String prezime,
                           @PathVariable(value = "indeks") String indeks){

        Ucesnici ucesnici = new Ucesnici(ime,prezime,indeks);
        return ucesniciRepository.save(ucesnici);
    }
    @GetMapping("/test")
    public String zadatak(){
        return "dodati zadatak";
    }

}
