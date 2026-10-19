# Run the Windows preview without requiring PowerShell script execution.
require 'rbconfig'

if Gem.win_platform?
  begin
    # Sass needs this encoding. Require it explicitly so a Windows policy block
    # produces a useful error rather than a conversion error or Ruby VM crash.
    require 'enc/utf_16be'
  rescue LoadError => error
    warn 'Ruby could not load its UTF-16BE encoding library.'
    warn error.message
    warn 'If Windows reports an Application Control block, that block must be resolved before Jekyll can run.'
    exit 1
  end
end

root = File.expand_path('..', __dir__)
Dir.chdir(root)
project_gems = File.join(root, '.bundle/gems/ruby', RbConfig::CONFIG['ruby_version'])
ENV['GEM_PATH'] = ([project_gems] + Gem.path).uniq.join(File::PATH_SEPARATOR)
ENV['BUNDLE_GEMFILE'] = File.join(__dir__, 'Gemfile.preview')
ENV['BUNDLE_IGNORE_CONFIG'] = '1'
Gem.clear_paths

ruby = RbConfig.ruby
unless system(ruby, '-S', 'bundle', 'check')
  unless system(ruby, '-S', 'bundle', 'install')
    warn 'Could not install the local preview dependencies.'
    exit 1
  end
end

args = ARGV.dup
build_only = args.delete('-Build')
port = '4000'
if (index = args.index('-Port'))
  port = args[index + 1]
  args.slice!(index, 2)
end
unless args.empty? && port && port.match?(/\A\d+\z/) && (1..65_535).cover?(port.to_i)
  warn 'Usage: preview.bat [-Build] [-Port 4001]'
  exit 1
end

command = if build_only
            ['build']
          else
            puts "Album preview: http://127.0.0.1:#{port}/photos.html (Ctrl+C to stop)"
            ['serve', '--host', '127.0.0.1', '--port', port, '--force_polling']
          end

success = system(ruby, '-rbundler/setup', '-e', "load Gem.bin_path('jekyll', 'jekyll')", '--', *command)
exit(success ? 0 : 1)
