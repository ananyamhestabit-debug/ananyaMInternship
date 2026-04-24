class Node:
    """Represents a node in the binary tree."""
    def __init__(self, value):
        # Initialize the node with a given value
        self.value = value
        # Set the left and right children to None by default
        self.left = None
        self.right = None


class BinaryTree:
    """Represents a binary tree."""
    def __init__(self, root):
        # Initialize the binary tree with a root node
        self.root = Node(root)
        # Initialize a counter for the node count
        self.node_count = 1

    def insert(self, value):
        # Insert a new node with a given value into the binary tree
        self._insert_recursive(self.root, value)

    def _insert_recursive(self, current_node, value):
        # Recursively find the correct position to insert the new node
        if value < current_node.value:
            # If the value is less than the current node's value, insert it to the left
            if current_node.left:
                self._insert_recursive(current_node.left, value)
            else:
                current_node.left = Node(value)
                self.node_count += 1
        else:
            # If the value is greater than or equal to the current node's value, insert it to the right
            if current_node.right:
                self._insert_recursive(current_node.right, value)
            else:
                current_node.right = Node(value)
                self.node_count += 1

    def preorder_traversal(self, start):
        """Performs a preorder traversal of the binary tree."""
        if start:
            # Print the current node's value
            print(start.value, end=" ")
            # Recursively traverse the left subtree
            self.preorder_traversal(start.left)
            # Recursively traverse the right subtree
            self.preorder_traversal(start.right)

    def inorder_traversal(self, start):
        """Performs an inorder traversal of the binary tree."""
        if start:
            # Recursively traverse the left subtree
            self.inorder_traversal(start.left)
            # Print the current node's value
            print(start.value, end=" ")
            # Recursively traverse the right subtree
            self.inorder_traversal(start.right)

    def postorder_traversal(self, start):
        """Performs a postorder traversal of the binary tree."""
        if start:
            # Recursively traverse the left subtree
            self.postorder_traversal(start.left)
            # Recursively traverse the right subtree
            self.postorder_traversal(start.right)
            # Print the current node's value
            print(start.value, end=" ")

    def find(self, value):
        # Find a node with a given value in the binary tree
        return self._find_recursive(self.root, value)

    def _find_recursive(self, current_node, value):
        # Recursively find the node with the given value
        if current_node is None:
            # If the current node is None, the value is not found
            return None
        elif value == current_node.value:
            # If the current node's value matches the given value, return the node
            return current_node
        elif value < current_node.value:
            # If the value is less than the current node's value, search in the left subtree
            return self._find_recursive(current_node.left, value)
        else:
            # If the value is greater than the current node's value, search in the right subtree
            return self._find_recursive(current_node.right, value)

    def remove(self, value):
        # Remove a node with a given value from the binary tree
        self.root = self._remove_recursive(self.root, value)
        self.node_count -= 1

    def _remove_recursive(self, current_node, value):
        # Recursively remove the node with the given value
        if current_node is None:
            # If the current node is None, the value is not found
            return current_node
        elif value < current_node.value:
            # If the value is less than the current node's value, remove the node from the left subtree
            current_node.left = self._remove_recursive(current_node.left, value)
            return current_node
        elif value > current_node.value:
            # If the value is greater than the current node's value, remove the node from the right subtree
            current_node.right = self._remove_recursive(current_node.right, value)
            return current_node
        else:
            # If the value matches the current node's value, remove the node
            if current_node.left:
                # If the node has a left child, replace it with the rightmost node in the left subtree
                current_node.value = self._find_rightmost(current_node.left).value
                current_node.left = self._remove_min(current_node.left)
            elif current_node.right:
                # If the node has a right child, replace it with the leftmost node in the right subtree
                current_node.value = self._find_leftmost(current_node.right).value
                current_node.right = self._remove_min(current_node.right)
            else:
                # If the node has no children, simply remove it
                return None
            return current_node

    def _remove_min(self, current_node):
        # Find the smallest node in the given subtree and remove it
        if current_node.left is None:
            # The smallest node is the current node
            return current_node
        else:
            # The smallest node is in the left subtree
            current_node.left = self._remove_min(current_node.left)
            return current_node

    def _find_leftmost(self, current_node):
        # Find the leftmost node in the given subtree
        while current_node.left:
            current_node = current_node.left
        return current_node

    def _find_rightmost(self, current_node):
        # Find the rightmost node in the given subtree
        while current_node.right:
            current_node = current_node.right
        return current_node


# Example usage:
tree = BinaryTree(1)
tree.insert(2)
tree.insert(3)
tree.insert(4)
tree.insert(5)
tree.insert(6)
tree.insert(7)

print("Preorder Traversal: ")
tree.preorder_traversal(tree.root)
print("\nInorder Traversal: ")
tree.inorder_traversal(tree.root)
print("\nPostorder Traversal: ")
tree.postorder_traversal(tree.root)

found_node = tree.find(5)
if found_node:
    print("\nNode found: ", found_node.value)
else:
    print("\nNode not found")

tree.remove(5)
print("\nPreorder Traversal after removing 5: ")
tree.preorder_traversal(tree.root)