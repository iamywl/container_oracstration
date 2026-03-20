package com.platform.controller;

import com.platform.model.Pipeline;
import com.platform.service.PipelineService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/pipelines")
public class PipelineController {

    private final PipelineService pipelineService;

    public PipelineController(PipelineService pipelineService) {
        this.pipelineService = pipelineService;
    }

    @GetMapping("/history")
    public ResponseEntity<List<Pipeline>> getHistory(
            @RequestParam(required = false) String app,
            @RequestParam(defaultValue = "20") int limit) {
        return ResponseEntity.ok(pipelineService.getHistory(app, limit));
    }

    @GetMapping("/deployments")
    public ResponseEntity<List<Map<String, Object>>> getDeployments(
            @RequestParam(required = false) String service,
            @RequestParam(required = false) String environment) {
        return ResponseEntity.ok(pipelineService.getDeployments(service, environment));
    }

    @GetMapping("/deployments/{service}/latest")
    public ResponseEntity<Map<String, Object>> getLatestDeployment(
            @PathVariable String service) {
        Map<String, Object> deployment = pipelineService.getLatestDeployment(service);
        if (deployment == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(deployment);
    }
}
