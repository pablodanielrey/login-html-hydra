from flask import Flask, jsonify, make_response, request
webapp = Flask(__name__)

@webapp.route('/gmail_send', methods=['POST'])
def gmail_send():
    """ http://googleapis.github.io/google-api-python-client/docs/dyn/gmail_v1.users.messages.html#send """

    response_ok = { # An email message.
        "threadId": "A String", # The ID of the thread the message belongs to. To add a message or draft to
            # a thread, the following criteria must be met:
            # <ol><li>The requested `threadId` must be specified on the
            # `Message` or `Draft.Message` you supply with your
            # request.</li>
            # <li>The `References` and `In-Reply-To` headers must
            # be set in compliance with the
            # <a href="https://tools.ietf.org/html/rfc2822">RFC 2822</a> standard.</li>
            # <li>The `Subject` headers must match.
            # @mutable gmail.users.messages.insert gmail.users.messages.send
            # @mutable gmail.users.drafts.create gmail.users.drafts.update
        "internalDate": "A String", # The internal message creation timestamp (epoch ms), which determines
            # ordering in the inbox.  For normal SMTP-received email, this represents the
            # time the message was originally accepted by Google, which is more reliable
            # than the `Date` header. However, for API-migrated mail, it can
            # be configured by client to be based on the `Date` header.
        "id": "A String", # The immutable ID of the message.
        "sizeEstimate": 42, # Estimated size in bytes of the message.
        "payload": { # A single MIME message part. # The parsed email structure in the message parts.
        "mimeType": "A String", # The MIME type of the message part.
        "parts": [ # The child MIME message parts of this part. This only applies to container
            # MIME message parts, for example `multipart/*`. For non-
            # container MIME message part types, such as `text/plain`, this
            # field is empty. For more information, see
            # <a href="http://www.ietf.org/rfc/rfc1521.txt">RFC 1521</a>.
            # Object with schema name: MessagePart
        ],
        "headers": [ # List of headers on this message part. For the top-level message part,
            # representing the entire message payload, it will contain the standard
            # RFC 2822 email headers such as `To`, `From`, and
            # `Subject`.
            {
            "name": "A String", # The name of the header before the `:` separator. For
                # example, `To`.
            "value": "A String", # The value of the header after the `:` separator. For example,
                # `someuser@example.com`.
            },
        ],
        "filename": "A String", # The filename of the attachment. Only present if this message part
            # represents an attachment.
        "partId": "A String", # The immutable ID of the message part.
        "body": { # The body of a single MIME message part. # The message part body for this part, which may be empty for
            # container MIME message parts.
            "size": 42, # Number of bytes for the message part data (encoding notwithstanding).
            "attachmentId": "A String", # When present, contains the ID of an external attachment that can be
                # retrieved in a separate `messages.attachments.get` request.
                # When not present, the entire content of the message part body is
                # contained in the data field.
            "data": "A String", # The body data of a MIME message part as a base64url encoded string.
                # May be empty for MIME container
                # types that have no message body or when the body data is sent as a
                # separate attachment. An attachment ID is present if the body data is
                # contained in a separate attachment.
        },
        },
        "historyId": "A String", # The ID of the last history record that modified this message.
        "snippet": "A String", # A short part of the message text.
        "raw": "A String", # The entire email message in an RFC 2822 formatted and base64url
            # encoded string. Returned in `messages.get` and
            # `drafts.get` responses when the `format=RAW`
            # parameter is supplied.
            # @mutable gmail.users.messages.insert gmail.users.messages.send
            # @mutable gmail.users.drafts.create gmail.users.drafts.update
        "labelIds": [ # List of IDs of labels applied to this message.
            # @mutable gmail.users.messages.insert gmail.users.messages.modify
        "A String",
        ],
    }

    return make_response(jsonify(response_ok)), 200



if __name__ == '__main__':
    webapp.run('0.0.0.0', 7777)