package org.plu.rest.controllers;

import org.plu.dao.UcesniciRepository;
import org.plu.entities.Ucesnici;
import org.plu.generator.TestGenerator;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;


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

    @GetMapping("/all")
    public List<Ucesnici> getAll(){
        return ucesniciRepository.findAll();
    }

    @GetMapping("/test")
    public String zadatak(){
        TestGenerator testGenerator = new TestGenerator();

        return testGenerator.generateTask();

    }

}
