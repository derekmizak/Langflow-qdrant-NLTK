import re
from typing import Dict, List, Any
from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Data


class TokenToHeadersComponent(Component):
    display_name = "Token to Headers"
    description = "Extract tokens from HTTP headers and format them for TableInput"
    documentation: str = "https://docs.langflow.org/components-custom-components"
    icon = "key"
    name = "TokenToHeadersComponent"

    inputs = [
        MessageTextInput(
            name="headers_input",
            display_name="Headers Input",
            info="HTTP headers dictionary containing tokens to extract",
            value="",
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Headers Output", name="headers_output", method="build_headers_output"),
    ]

    def extract_tokens_from_cookies(self, set_cookie_header: str) -> Dict[str, str]:
        """Extract accessToken and refreshToken from set-cookie header"""
        tokens = {}
        
        # Handle empty or None input
        if not set_cookie_header:
            return tokens
        
        # Extract accessToken - try multiple patterns
        access_patterns = [
            r'accessToken=([^;,\s]+)',  # Standard pattern
            r'"accessToken":\s*"([^"]+)"',  # JSON pattern
            r'accessToken:\s*([^;,\s]+)',  # Colon pattern
        ]
        
        for pattern in access_patterns:
            access_token_match = re.search(pattern, set_cookie_header)
            if access_token_match:
                tokens['accessToken'] = access_token_match.group(1).strip()
                break
        
        # Extract refreshToken - try multiple patterns
        refresh_patterns = [
            r'refreshToken=([^;,\s]+)',  # Standard pattern
            r'"refreshToken":\s*"([^"]+)"',  # JSON pattern
            r'refreshToken:\s*([^;,\s]+)',  # Colon pattern
        ]
        
        for pattern in refresh_patterns:
            refresh_token_match = re.search(pattern, set_cookie_header)
            if refresh_token_match:
                tokens['refreshToken'] = refresh_token_match.group(1).strip()
                break
        
        return tokens

    def build_headers_output(self) -> Data:
        """Build the output formatted for TableInput"""
        try:
            # Parse the input - it could be a string representation of a dict or actual dict
            headers_input = self.headers_input
            
            # Handle different input types
            if isinstance(headers_input, str):
                # Try to evaluate string as dict
                import ast
                import json
                try:
                    # Try JSON parsing first
                    headers_dict = json.loads(headers_input)
                except json.JSONDecodeError:
                    try:
                        # Try ast.literal_eval
                        headers_dict = ast.literal_eval(headers_input)
                    except (ValueError, SyntaxError):
                        try:
                            # Last resort: eval (be careful in production)
                            headers_dict = eval(headers_input)
                        except:
                            # If all parsing fails, treat as plain text
                            headers_dict = {'raw_input': headers_input}
            elif isinstance(headers_input, dict):
                headers_dict = headers_input
            else:
                # Handle other types (like Data objects)
                if hasattr(headers_input, 'value'):
                    headers_dict = headers_input.value if isinstance(headers_input.value, dict) else {'data': str(headers_input.value)}
                else:
                    headers_dict = {'data': str(headers_input)}
            
            # Extract tokens from set-cookie header
            set_cookie = headers_dict.get('set-cookie', '')
            tokens = self.extract_tokens_from_cookies(set_cookie)
            
            # Prepare the output format for TableInput
            output_data = []
            
            # Add Authorization header if accessToken exists
            if 'accessToken' in tokens:
                output_data.append({
                    "key": "Authorization",
                    "value": f"Bearer {tokens['accessToken']}"
                })
            
            # Add Cookie header if both tokens exist
            if 'accessToken' in tokens and 'refreshToken' in tokens:
                cookie_value = f"refreshToken={tokens['refreshToken']}; accessToken={tokens['accessToken']}"
                output_data.append({
                    "key": "Cookie",
                    "value": cookie_value
                })
            
            # If no tokens found, add error info
            if not tokens:
                output_data.append({
                    "key": "Error",
                    "value": f"No tokens found in headers"
                })
            
            # Create Data object with the formatted output
            result = Data(value=output_data)
            self.status = f"Extracted {len(output_data)} headers"
            return result
            
        except Exception as e:
            error_msg = f"Error processing headers: {str(e)}"
            self.status = error_msg
            # Return debug info even on error
            return Data(value=[{
                "key": "Error", 
                "value": f"{error_msg}. Input: {str(headers_input)[:200]}"
            }])