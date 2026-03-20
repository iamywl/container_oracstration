package com.platform.service;

import com.platform.model.Container;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.HashMap;

@Service
public class ContainerService {

    private final JdbcTemplate jdbc;

    public ContainerService(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    private final RowMapper<Container> containerMapper = (rs, rowNum) -> {
        Container c = new Container();
        c.setId(rs.getLong("id"));
        c.setName(rs.getString("name"));
        c.setService(rs.getString("service"));
        c.setImage(rs.getString("image"));
        c.setStatus(rs.getString("status"));
        c.setReplicaIdx(rs.getInt("replica_idx"));
        return c;
    };

    public List<Container> findAll() {
        return jdbc.query("SELECT * FROM containers ORDER BY created_at DESC", containerMapper);
    }

    public List<Container> findByService(String service) {
        return jdbc.query(
            "SELECT * FROM containers WHERE service = ? ORDER BY replica_idx",
            containerMapper, service
        );
    }

    public List<Container> findByStatus(String status) {
        return jdbc.query(
            "SELECT * FROM containers WHERE status = ?",
            containerMapper, status
        );
    }

    public Map<String, Object> getOverview() {
        Map<String, Object> overview = new HashMap<>();

        Integer total = jdbc.queryForObject(
            "SELECT COUNT(*) FROM containers", Integer.class
        );
        Integer running = jdbc.queryForObject(
            "SELECT COUNT(*) FROM containers WHERE status = 'running'", Integer.class
        );
        Integer stopped = jdbc.queryForObject(
            "SELECT COUNT(*) FROM containers WHERE status != 'running'", Integer.class
        );

        overview.put("total", total != null ? total : 0);
        overview.put("running", running != null ? running : 0);
        overview.put("stopped", stopped != null ? stopped : 0);
        overview.put("containers", findAll());

        return overview;
    }

    public List<Map<String, Object>> getEvents(String containerName, int limit) {
        if (containerName != null) {
            return jdbc.queryForList(
                "SELECT * FROM events WHERE container_name = ? ORDER BY created_at DESC LIMIT ?",
                containerName, limit
            );
        }
        return jdbc.queryForList(
            "SELECT * FROM events ORDER BY created_at DESC LIMIT ?", limit
        );
    }
}
