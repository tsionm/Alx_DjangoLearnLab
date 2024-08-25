## Permissions and Groups Setup

### Custom Permissions

The following custom permissions have been added to the `Book` model:
- `can_view`: Allows viewing of book details.
- `can_create`: Allows creation of new books.
- `can_edit`: Allows editing of existing books.
- `can_delete`: Allows deletion of books.

### Groups and Permissions

- **Editors**: Assigned `can_create` and `can_edit` permissions.
- **Viewers**: Assigned `can_view` permission.
- **Admins**: Assigned all permissions (`can_view`, `can_create`, `can_edit`, `can_delete`).

### Views and Permissions

Permissions are enforced in the following views using the `@permission_required` decorator:
- `view_book`: Requires `can_view` permission.
- `create_book`: Requires `can_create` permission.
- `edit_book`: Requires `can_edit` permission.
- `delete_book`: Requires `can_delete` permission.