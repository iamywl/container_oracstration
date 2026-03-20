package com.platform.controller;

import com.platform.model.Container;
import com.platform.service.ContainerService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/containers")
public class ContainerController {

    private final ContainerService containerService;

    public ContainerController(ContainerService containerService) {
        this.containerService = containerService;
    }

    @GetMapping
    public ResponseEntity<List<Container>> listContainers(
            @RequestParam(required = false) String service,
            @RequestParam(required = false) String status) {
        if (service != null) {
            return ResponseEntity.ok(containerService.findByService(service));
        }
        if (status != null) {
            return ResponseEntity.ok(containerService.findByStatus(status));
        }
        return ResponseEntity.ok(containerService.findAll());
    }

    @GetMapping("/overview")
    public ResponseEntity<Map<String, Object>> getOverview() {
        return ResponseEntity.ok(containerService.getOverview());
    }

    @GetMapping("/events")
    public ResponseEntity<List<Map<String, Object>>> getEvents(
            @RequestParam(required = false) String container,
            @RequestParam(defaultValue = "50") int limit) {
        return ResponseEntity.ok(containerService.getEvents(container, limit));
    }
}
