require 'liquid'
Dir.glob('_posts/*ML-Series*.md').each do |f|
  content = File.read(f)
  begin
    Liquid::Template.parse(content)
  rescue => e
    puts "#{f}: #{e}"
  end
end
