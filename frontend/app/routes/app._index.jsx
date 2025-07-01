import { json, LoaderFunctionArgs } from "@remix-run/node";
import { Page, Layout, Card, Button } from "@shopify/polaris";
import { authenticate } from "../shopify.server";

export async function loader({ request }) {
  await authenticate.admin(request);
  return json({});
}

export async function action({ request }) {
  const { session } = await authenticate.admin(request);
  
  // Get session token for backend auth
  const sessionToken = await session.getSessionToken();
  
  // Call Python backend
  const response = await fetch(`${process.env.BACKEND_URL}/api/process`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${sessionToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ action: "test" }),
  });
  
  const result = await response.json();
  return json(result);
}

export default function Index() {
  return (
    <Page title="My App">
      <Layout>
        <Layout.Section>
          <Card>
            <Button submit>Test Backend Connection</Button>
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
}