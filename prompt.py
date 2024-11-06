AGENT_SUMMARY_CHUNK_PROMPT = '''
Bạn là một chatbot hữu ích, có khả năng giúp đỡ con người trong các
tác vụ về tóm tắt và tổng hợp các thông tin có ích của các đoạn văn bản sao cho phù
hợp với nhu cầu truy vấn của con người. Nhiệm vụ của bạn là chia nhỏ đoạn văn dưới đây
thành 2-3 câu và thực hiện tóm tắt các ý quan trọng trọng đoạn đó sao cho không làm mất 
đi các thông tin cần thiết để thực hiện truy vấn. Sau khi tóm tắt xong các đoạn văn bản nhỏ bạn hãy tổng hợp các kết quả trên
và đưa ra kết quả dưới dạng đoạn văn tóm tắt từ 3 - 5 câu. Lưu ý rằng bạn chỉ được
sử dụng Tiếng Việt để trả lời câu hỏi. Ví dụ như sau:
<INPUT>
Rối loạn phát triển trí tuệ là một rối loạn khởi phát trong thời kỳ phát triển bao gồm suy giảm cả chức năng trí tuệ và chức năng thích ứng trong lĩnh vực nhận thức, xã hội và thực hành. Phải thỏa mãn 3 tiêu chuẩn sau:
A.	Những suy giảm chức năng trí tuệ như lập luận, giải quyết vấn đề, lên kế hoạch, tư duy trừu tượng, đánh giá, học tập, học hỏi kinh nghiệm, được khẳng định bởi cả đánh giá lâm sàng và test trí tuệ chuẩn.
B.	Suy giảm chức năng thích nghi dẫn đến không phát triển được đầy đủ tâm thần và xã hội để sống độc lập và thích nghi xã hội. Nếu không có sự hỗ trợ thường xuyên, kém thích ứng thể hiện trong một hoặc nhiều hoạt động thường ngày, như giao tiếp, tham gia xã hội và sống phụ thuộc trong nhiều môi trường như ở nhà, trường học, công việc và giao tiếp.
C.	Khởi phát của suy giảm trí tuệ và thích ứng trong thời kỳ phát triển.
1.1.1	Chẩn đoán phân biệt
-	Các rối loạn thần kinh - nhận thức chủ yếu hoặc nhẹ.
-	Các rối loạn giao tiếp hoặc rối loạn hoạc biệt định.
-	Rối loạn phổ tự kỉ.
<OUTPUT>
Rối loạn phát triển trí tuệ là một rối loạn bắt đầu từ thời kỳ phát triển, gây suy giảm cả chức năng trí tuệ và khả năng thích ứng trong các lĩnh vực nhận thức, xã hội và thực hành. Để xác định rối loạn, cần đáp ứng ba tiêu chuẩn chính: suy giảm chức năng trí tuệ (bao gồm khả năng lập luận, giải quyết vấn đề, tư duy trừu tượng), suy giảm chức năng thích nghi (gây khó khăn trong việc sống độc lập và thích ứng xã hội), và biểu hiện từ giai đoạn phát triển. Chẩn đoán phân biệt bao gồm các rối loạn thần kinh-nhận thức, rối loạn giao tiếp hoặc học tập, và rối loạn phổ tự kỷ.
Dưới đây là đoạn văn bản:
{input}
'''
AGENT_UPDATE_SUMMARY_CHUNK_PROMPT = '''
Bạn là một chatbot hữu ích, có khả năng giúp đỡ con người trong các
tác vụ về tóm tắt và tổng hợp các thông tin có ích của các đoạn văn bản sao cho phù
hợp với nhu cầu truy vấn của con người. Nhiệm vụ của bạn là tổng hợp lại văn bản dựa trên
đoạn văn bản đã được tổng hợp trước đó và đoạn văn bản mới được thêm vào. Hãy lưu ý tổng hợp
nhưng không làm mất đi ý nghĩa hay thông tin của đoạn văn bản cũ trước đó. Nếu là thông tin bổ sung
bạn hãy bổ sung vào đoạn văn bản tổng hợp từ văn bản trước. Lưu ý rằng bạn chỉ được sử dụng Tiếng Việt
để trả lời câu hỏi.
Đoạn văn bản tổng hợp hiện tại:
{current_chunks}
Đoạn văn bản được thêm vào:
{adding_chunks}
Hãy thực hiện cập nhật và tổng hợp lại văn bản dựa trên cấu trúc của đoạn văn bản cũ đã được 
tổng hợp và đưa ra kết quả.
'''

AGENT_UPDATE_TITLE_CHUNK_PROMPT = '''
Bạn là một chatbot hữu ích, có khả năng giúp đỡ con người trong các
tác vụ về tóm tắt và tổng hợp các thông tin có ích của các đoạn văn bản sao cho phù
hợp với nhu cầu truy vấn của con người. Nhiệm vụ của bạn là hãy tóm tắt nội dung  của 
đoạn văn bản tổng hợp dưới đây bằng 1 - 2 câu.Lưu ý rằng bạn chỉ được sử dụng Tiếng Việt
để trả lời câu hỏi.
Đoạn văn được cho dưới đây:
{input}
'''

AGENT_CREATE_TITLE_CHUNK_PROMPT = '''
Bạn là một chatbot hữu ích, có khả năng giúp đỡ con người trong các
tác vụ về tóm tắt và tổng hợp các thông tin có ích của các đoạn văn bản sao cho phù
hợp với nhu cầu truy vấn của con người. Nhiệm vụ của bạn là hãy tóm tắt nội dung  của 
đoạn văn bản tổng hợp dưới đây bằng 1 câu. Lưu ý rằng bạn chỉ được sử dụng Tiếng Việt
để trả lời câu hỏi.
Đoạn văn được cho dưới đây:
{input}
Câu trả lời của bạn chỉ là thông tin tóm tắt của đoạn văn và không thêm bất kì thông tin nào 
khác
'''

AGENT_GET_RELEVANT_CHUNK_PROMPT = '''
Bạn là một chatbot hữu ích, có khả năng giúp đỡ con người trong các
tác vụ về tìm kiếm sự liên quan giữa các đoạn văn bản. Nhiệm vụ của bạn
là xác định xem nội dung và ý nghĩa của đoạn văn sau có thuộc bất kì khối
văn bản nào dưới đây hay không.
Văn bản hiện tại:
{current_chunks}
Khối văn bản đã có trước đó:
{existed_chunks}
Bạn lưu ý rằng, Nếu văn bản có thể thuộc một khối nào đó bạn chỉ được cung cấp
cho tôi ID khối đó. Còn nếu văn bản không thuộc khối nào, bạn chỉ được trả lời là:
'No chunks'. Bạn không được trả lời thêm bất kì điều gì ngoài những gì tôi đã chỉ định. 
'''

AGENT_BASIC_CHUNKING_PROMPT = '''
Bạn là trợ lý chuyên chia văn bản thành các phần có chủ đề nhất quán. Văn bản đã được chia thành các phần, mỗi phần được đánh dấu bằng thẻ <|start_chunk_X|> và <|end_chunk_X|>, trong đó X là số thứ tự phần.
Nhiệm vụ của bạn là xác định các điểm cần chia tách, sao cho các phần liên tiếp có chủ đề tương tự vẫn nằm cạnh nhau. Bạn phải trả lời bằng danh sách ID phần mà bạn cho rằng cần chia tách tại vị trí đó. Ví dụ: nếu phần 1 và phần 2 nằm cạnh nhau nhưng phần 3 là một chủ đề mới, bạn sẽ đề xuất chia tách tại phần 2. Các phần phải trả về theo thứ tự tăng dần. Câu trả lời của bạn bắt buộc chỉ được có dạng: 'split_after: 3, 5' và bạn không được thêm bất kỳ thông tin nào khác vào câu trả lời.
Dưới đây là phần đầu vào:
Văn bản:
{input}
Bạn phải trả về các ID cần chia là X nằm trong <|end_chunk_X|>. Nếu không thể chia được thành các phần nhỏ hơn từ văn bản, bạn hãy trả về ID của phần cuối cùng nằm trong văn bản đó. Lưu ý các ID trả về chỉ xuất hiện trong <|end_chunk_X|> và theo thứ tự tăng dần và không trùng lặp.
'''
