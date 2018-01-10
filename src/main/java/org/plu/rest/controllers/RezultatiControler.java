package org.plu.rest.controllers;


import org.plu.dao.ResenjeRepository;
import org.plu.dao.RezultatiRepository;
import org.plu.entities.Resenje;
import org.plu.entities.Rezultati;
import org.plu.generator.ResultsGenerator;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.List;


@RestController
@RequestMapping("/rezultati")
public class RezultatiControler {

    @Autowired
    private RezultatiRepository rezultatiRepository;

    @Autowired
    private ResenjeRepository resenjeRepository;

    @GetMapping("/new/{student}/{rezultat}")
    public void addNew(@PathVariable(value = "student") String student, @PathVariable(value = "rezultat") int rezultat){

        List<Resenje> resenje = resenjeRepository.findAll();

        for (Resenje r : resenje){
            System.out.println(r.getResenje());
        }
        Rezultati rezultati = new Rezultati(student,rezultat);

        rezultatiRepository.save(rezultati);

    }
    @GetMapping("/oceni")
    public String oceniSVE(){
        List<Resenje> resenje = resenjeRepository.findAll();
        ResultsGenerator resultsGenerator = new ResultsGenerator();
        for (Resenje r : resenje){
           // System.out.println(r.getResenje());
            r.getResenje().replace('*',';');
            r.getResenje().replace(' ','\n');
            resultsGenerator.isItGood(r.getResenje());


        }
        return "ALL DONE";

    }

    @GetMapping("/all")
    public List<Rezultati> getAll(){
       return rezultatiRepository.findAll();
    }


}
