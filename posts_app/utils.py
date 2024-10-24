def build_comment_tree(comments):
    comments = [item.to_json() for item in comments]
    # Create a dictionary to store children of each comment
    comment_dict = {comment["id"]: comment for comment in comments}
    tree_comments = []

    for comment in comments:
        parent_id = comment.pop("parent", None)
        if parent_id is None:
            tree_comments.append(comment)
        else:
            comment_dict[parent_id]['answers'].append(comment)
    return tree_comments
