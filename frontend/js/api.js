const API_BASE_URL = "http://localhost:5000/api";

const TransitAPI = {
    async getNetwork() {
        const response = await fetch(`${API_BASE_URL}/network`);
        return await response.json();
    },

    async getLines() {
        const response = await fetch(`${API_BASE_URL}/lines`);
        return await response.json();
    },

    async findPath(startNode, endNode) {
        const response = await fetch(`${API_BASE_URL}/find-path`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ start_node: startNode, end_node: endNode })
        });
        return await response.json();
    },

    async toggleLine(lineName, disabled) {
        const response = await fetch(`${API_BASE_URL}/admin/toggle-line`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ line: lineName, disabled: disabled })
        });
        return await response.json();
    }
};
