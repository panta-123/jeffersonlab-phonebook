// openapi-ts.config.ts
import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
  // Point to the local OpenAPI specification file (as per previous instructions)
  input: './src/openapi.json',
  // Directory where the client will be generated
  output: './src/client',
  // Use 'httpClient' instead of 'client' for Axios
  httpClient: 'axios',
  // Optional: Give a name to your generated client
  name: 'VulcanApiClient',
});
