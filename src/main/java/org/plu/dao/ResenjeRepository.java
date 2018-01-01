package org.plu.dao;

import org.plu.entities.Resenje;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ResenjeRepository extends JpaRepository<Resenje,Integer>{
}
