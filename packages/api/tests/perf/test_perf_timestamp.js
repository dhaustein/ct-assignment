
import { check, group, sleep } from "k6";
import http from "k6/http";

const BASE_URL = "https://helloacm.com/api/unix-timestamp-converter/";

export const options = {
    stages: [
        { duration: '1m', target: 20 },
        { duration: '3m', target: 20 },
        { duration: '1m', target: 0 },
    ],
    thresholds: {
        'http_req_duration': ['p(95)<250'],
        'checks': ['rate>0.95'],
        'group_duration{group:::Visit API page}': ['p(95)<100'],
        'group_duration{group:::Convert valid timestamp}': ['p(95)<200'],
        'group_duration{group:::Handle conversion error}': ['p(95)<200'],
        'group_duration{group:::Handle 404 error}': ['p(95)<150'],
    },
};

/**
 * Sleep functions to simulate different user behaviors
 */
function sleepBrowsing() {
    // 1-3 seconds for casual browsing
    sleep(Math.random() * 2 + 1);
}

function sleepProcessing() {
    // 1-4 seconds for processing results
    sleep(Math.random() * 3 + 1);
}

function sleepErrorHandling() {
    // 1-3 seconds when encountering errors
    sleep(Math.random() * 2 + 1);
}

function sleepQuickExit() {
    // 0.5-1.5 seconds for quick exits on errors
    sleep(Math.random() * 1 + 0.5);
}

/**
 * Performance test function that emulates different user journeys:
 * - Group 1: Users who just visit the API page
 * - Group 2: Users who visit and convert a valid timestamp
 * - Group 3: Users who visit and attempt to convert an invalid timestamp (error scenario)
 * - Group 4: Users who visit a non-existent endpoint (404 scenario)
 */
export default function () {
    // Randomly select which user journey to follow
    const userType = Math.random();

    if (userType < 0.25) {

        group("Visit the API page", () => {
            const response = http.get(BASE_URL);

            check(response, {
                "API page status is 200": (r) => r.status === 200,
                "API page loads successfully": (r) => r.body.length > 0,
            });

            sleepBrowsing();
        });

    } else if (userType < 0.50) {

        group("Convert valid timestamp", () => {
            const response = http.get(`${BASE_URL}?cached&s=1451613802`);

            check(response, {
                "valid conversion status is 200": (r) => r.status === 200,
                "timestamp is converted correctly": (r) =>
                    r.body.includes("2016-01-01 02:03:22"),
            });

            sleepProcessing();
        });

    // TODO also test conversion from date time to Unix timestamp

    } else if (userType < 0.75) {

        group("Handle conversion error", () => {
            const response = http.get(`${BASE_URL}?cached&s=invalid`);

            check(response, {
                "invalid timestamp handled gracefully": (r) =>
                    r.status === 200 || r.status === 400,
                "error response is not empty": (r) => r.body.length > 0,
            });

            sleepErrorHandling();
        });

    } else {

        group("Handle 404 error", () => {
            const response = http.get("https://helloacm.com/api/nonexistent-endpoint/");

            check(response, {
                "404 status for non-existent endpoint": (r) => r.status === 404,
                "404 response is handled": (r) => r.body.length > 0,
            });

            sleepQuickExit();
        });
    }
}
