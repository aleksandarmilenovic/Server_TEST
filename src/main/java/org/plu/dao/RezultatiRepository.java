package org.plu.dao;

import org.plu.entities.Rezultati;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface RezultatiRepository extends JpaRepository<Rezultati,Integer>{
}
