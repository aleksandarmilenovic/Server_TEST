package org.plu.dao;

import org.plu.entities.Ucesnici;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UcesniciRepository extends JpaRepository<Ucesnici,Integer>{
}
