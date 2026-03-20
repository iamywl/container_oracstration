package com.platform.model;

import java.time.LocalDateTime;

public class Container {
    private Long id;
    private String name;
    private String service;
    private String image;
    private String status;
    private int replicaIdx;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public Container() {}

    public Container(String name, String service, String image, String status) {
        this.name = name;
        this.service = service;
        this.image = image;
        this.status = status;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getService() { return service; }
    public void setService(String service) { this.service = service; }
    public String getImage() { return image; }
    public void setImage(String image) { this.image = image; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public int getReplicaIdx() { return replicaIdx; }
    public void setReplicaIdx(int replicaIdx) { this.replicaIdx = replicaIdx; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}
