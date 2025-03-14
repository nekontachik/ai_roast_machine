#!/bin/bash
# Script to create a release archive for AI Roast Machine

VERSION="1.0.0"
ARCHIVE_NAME="ai_roast_machine-${VERSION}"

echo "Creating release archive for AI Roast Machine ${VERSION}..."

# Create a temporary directory
mkdir -p tmp/${ARCHIVE_NAME}

# Copy files to the temporary directory
cp -r src tmp/${ARCHIVE_NAME}/
cp -r tests tmp/${ARCHIVE_NAME}/
cp -r docker tmp/${ARCHIVE_NAME}/
cp -r scripts tmp/${ARCHIVE_NAME}/
cp -r docs tmp/${ARCHIVE_NAME}/
cp .env.example tmp/${ARCHIVE_NAME}/.env.example
cp README.md tmp/${ARCHIVE_NAME}/
cp RELEASE_NOTES.md tmp/${ARCHIVE_NAME}/
cp requirements.txt tmp/${ARCHIVE_NAME}/
cp run_menu.py tmp/${ARCHIVE_NAME}/
cp run_tests.py tmp/${ARCHIVE_NAME}/
cp open_reports.py tmp/${ARCHIVE_NAME}/
cp cleanup.sh tmp/${ARCHIVE_NAME}/

# Create the archive
cd tmp
zip -r ../${ARCHIVE_NAME}.zip ${ARCHIVE_NAME}
cd ..

# Create a tarball
cd tmp
tar -czf ../${ARCHIVE_NAME}.tar.gz ${ARCHIVE_NAME}
cd ..

# Clean up
rm -rf tmp

echo "Release archives created:"
echo "- ${ARCHIVE_NAME}.zip"
echo "- ${ARCHIVE_NAME}.tar.gz"
echo ""
echo "You can now upload these files to the GitHub release." 