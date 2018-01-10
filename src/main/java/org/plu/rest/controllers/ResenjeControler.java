package org.plu.rest.controllers;

import org.plu.dao.ResenjeRepository;
import org.plu.entities.Resenje;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;


@RestController
@RequestMapping("/resenje")
public class ResenjeControler {

    @Autowired
    private ResenjeRepository  resenjeRepository;

    @GetMapping("/new/{student}/{resenje}")
    public Resenje addResult(@PathVariable(value = "student") String student, @PathVariable(value = "resenje") String resenje){
        resenje.replace('*',';');
        Resenje resenje1 = new Resenje(student,resenje);

        return resenjeRepository.save(resenje1);
    }


    @GetMapping("/all")
    public List<Resenje> getALl(){

        return resenjeRepository.findAll();
    }


}
