package org.plu.rest.controllers;


import org.plu.dao.RezultatiRepository;
import org.plu.entities.Rezultati;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;


@RestController
@RequestMapping("/rezultati")
public class RezultatiControler {

    @Autowired
    private RezultatiRepository rezultatiRepository;

    @GetMapping("/new/{student}/{rezultat}")
    public Rezultati addNew(@PathVariable(value = "student") String student, @PathVariable(value = "rezultat") int rezultat){

        Rezultati rezultati = new Rezultati(student,rezultat);

       return rezultatiRepository.save(rezultati);

    }

    @GetMapping("/all")
    public List<Rezultati> getAll(){
       return rezultatiRepository.findAll();
    }


}
