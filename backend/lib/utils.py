def split_strings_with_max_length(input_list, max_length=10000):
    """
    Splits each string in the input list by '.' and further splits
    substrings if they exceed the specified max_length.

    Args:
      input_list: A list of strings.
      max_length: The maximum allowed length for each substring.
                 Defaults to 40.

    Returns:
      A list of strings, where each string is split by '.' and further
      split if its length exceeds max_length.
    """
    output_list = []
    for string in input_list:
        parts = string.split(".")
        for part in parts:
            if len(part) > max_length:
                while len(part) > max_length:
                    output_list.append(part[:max_length])
                    part = part[max_length:]
                output_list.append(part)
            else:
                output_list.append(part)
    return output_list
