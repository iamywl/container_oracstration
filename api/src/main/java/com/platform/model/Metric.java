package com.platform.model;

import java.time.LocalDateTime;

public class Metric {
    private Long id;
    private String containerName;
    private double cpuPercent;
    private double memoryUsageMb;
    private double memoryPercent;
    private long networkRx;
    private long networkTx;
    private LocalDateTime collectedAt;

    public Metric() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getContainerName() { return containerName; }
    public void setContainerName(String containerName) { this.containerName = containerName; }
    public double getCpuPercent() { return cpuPercent; }
    public void setCpuPercent(double cpuPercent) { this.cpuPercent = cpuPercent; }
    public double getMemoryUsageMb() { return memoryUsageMb; }
    public void setMemoryUsageMb(double memoryUsageMb) { this.memoryUsageMb = memoryUsageMb; }
    public double getMemoryPercent() { return memoryPercent; }
    public void setMemoryPercent(double memoryPercent) { this.memoryPercent = memoryPercent; }
    public long getNetworkRx() { return networkRx; }
    public void setNetworkRx(long networkRx) { this.networkRx = networkRx; }
    public long getNetworkTx() { return networkTx; }
    public void setNetworkTx(long networkTx) { this.networkTx = networkTx; }
    public LocalDateTime getCollectedAt() { return collectedAt; }
    public void setCollectedAt(LocalDateTime collectedAt) { this.collectedAt = collectedAt; }
}
