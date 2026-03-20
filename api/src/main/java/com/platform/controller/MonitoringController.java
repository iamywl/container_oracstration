package com.platform.controller;

import com.platform.model.Metric;
import com.platform.service.MonitoringService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/monitoring")
public class MonitoringController {

    private final MonitoringService monitoringService;

    public MonitoringController(MonitoringService monitoringService) {
        this.monitoringService = monitoringService;
    }

    @GetMapping("/metrics/{containerName}")
    public ResponseEntity<List<Metric>> getMetrics(
            @PathVariable String containerName,
            @RequestParam(defaultValue = "100") int limit) {
        return ResponseEntity.ok(monitoringService.getMetrics(containerName, limit));
    }

    @GetMapping("/metrics/{containerName}/avg")
    public ResponseEntity<Map<String, Object>> getMetricAvg(
            @PathVariable String containerName,
            @RequestParam(defaultValue = "5") int minutes) {
        return ResponseEntity.ok(monitoringService.getMetricAvg(containerName, minutes));
    }

    @GetMapping("/alerts")
    public ResponseEntity<List<Map<String, Object>>> getActiveAlerts() {
        return ResponseEntity.ok(monitoringService.getActiveAlerts());
    }

    @GetMapping("/alerts/summary")
    public ResponseEntity<Map<String, Object>> getAlertSummary() {
        return ResponseEntity.ok(monitoringService.getAlertSummary());
    }

    @GetMapping("/dashboard")
    public ResponseEntity<Map<String, Object>> getDashboard() {
        return ResponseEntity.ok(monitoringService.getDashboardData());
    }
}
